from fastapi import FastAPI, Request
import uvicorn
import os
from dotenv import load_dotenv
import logging
from bot.logs import Logger
from contextlib import asynccontextmanager
from db.controller import MongoController

logging.getLogger("uvicorn.access").handlers = []
logging.getLogger("uvicorn.error").handlers = []
logging.getLogger("uvicorn").propagate = False

log = Logger("webserver.log", 3)

@asynccontextmanager
async def lifespan(app: FastAPI):
  log.log("Web-Server Online!")

  yield

  if hasattr(app, "db") and hasattr(app.db, "client"):
    app.db.client.close()
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

async def run_app(db: MongoController):
  app.db = db
  
  config = uvicorn.Config(
    app, host="0.0.0.0", port=PORT, log_config=None
    )
  server = uvicorn.Server(config)
  await server.serve()