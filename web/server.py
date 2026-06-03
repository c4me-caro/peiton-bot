from fastapi import FastAPI, Request, Header, status, HTTPException
import uvicorn
import os
from dotenv import load_dotenv
import logging
from bot.logs import Logger
from contextlib import asynccontextmanager
from db.controller import MongoController
from typing import Optional
from web.secutils import manage_alert, generate_alert_id, validate_token
from web.objects import Alerts, Welcome
from db.objects import MongoAlerts, MongoWelcome, MongoGuild

logging.getLogger("uvicorn.access").handlers = []
logging.getLogger("uvicorn.error").handlers = []
logging.getLogger("uvicorn").propagate = False

log = Logger("webserver.log", 3)

@asynccontextmanager
async def lifespan(app: FastAPI):
  log.log("Web-Server Online!")

  yield

  if hasattr(app.bot, "db") and hasattr(app.bot.db, "client"):
    app.bot.db.client.close()
    log.log("Conexión con MongoDB cerrada correctamente.")

load_dotenv()
PORT = int(os.getenv("WEB_PORT"))

app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None)

@app.middleware("http")
async def request_logs(request: Request, call_next):
  forwarded = request.headers.get("X-Forwarded-For")
  if forwarded:
    client_ip = forwarded.split(",")[0].strip()
  else:
    client_ip = request.client.host

  destination = request.url.path
  response = await call_next(request)
  status = response.status_code

  log.log(f"HTTP [{status}] - {request.method} from {client_ip} to {destination}")

  return response

@app.get("/")
async def home():
  return {"Hello": "World!"}

@app.get("/api/guilds/get")
async def get_guild(Authorization: str = Header(None), guild_id: int = 0):
  token = Authorization
  validate_token = await validate_token(app.db, token, guild_id)
  if not validate_token:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED, 
      detail="Token no valido"
    )

  if guild_id == 0:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="ID de servidor no proporcionado"
    )

  docs = await app.bot.db.get_document("servers", {"id":guild_id})
  if len(docs) == 0:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Servidor no encontrado"
    )
  
  doc = docs[0]
  doc.pop("_id", None)
  data = MongoGuild(**doc)
  return {"name": data.name, "icon": data.icon}

@app.post("/api/welcomes/create")
async def create_welcome(Authorization: str = Header(None), data: Optional[Welcome] = None):
  token = Authorization
  validate_token = await validate_token(app.db, token, data.guild_id)
  if not validate_token:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED, 
      detail="Token no valido"
    )

  doc = MongoWelcome(
    guild_id=data.guild_id,
    description=data.description,
    image_url=data.image_url,
    channel=data.channel
  )

  _ = await app.bot.db.add_document("welcome", doc.to_dict())
  return {"sucess": True}

@app.post("/api/alerts/create")
async def create_alert(Authorization: str = Header(None), alert: Optional[Alerts] = None):
  token = Authorization
  validate_token = await validate_token(app.bot.db, token, alert.guild_id)
  if not validate_token:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED, 
      detail="Token no valido"
    )

  id = generate_alert_id()
  doc = MongoAlerts(
    id=id,
    guild_id=alert.guild_id,
    title=alert.title,
    channel=alert.channel,
    image_url=alert.image_url
  )

  _ = await app.bot.db.add_document("alerts", doc.to_dict())
  return {"sucess": True}

@app.post("/api/alerts/delete")
async def delete_alert(Authorization: str = Header(None), alert: Optional[Alerts] = None):
  token = Authorization
  validate_token = await validate_token(app.bot.db, token, alert.guild_id)
  if not validate_token:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED, 
      detail="Token no valido"
    )

  _ = app.bot.db.drop_document("alerts", {"id": alert_id})
  return {"sucess": True}

@app.get("/api/alerts/generate")
async def call_alert(Authorization: str = Header(None), id: str = "", message: Optional[str] = None):
  token = Authorization
  if not token: 
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED, 
      detail="Token no proporcionado"
    )

  if not app.bot.is_ready():
    raise HTTPException(
      status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
      detail="El bot no está listo para enviar alertas" 
    )

  await manage_alert(app.bot, log, token, id, message)
  return {"sucess": True}

async def run_app(bot):
  app.bot = bot
  
  config = uvicorn.Config(
    app, host="0.0.0.0", port=PORT, log_config=None
    )
  server = uvicorn.Server(config)
  await server.serve()