import secrets 
from db.objects import MongoAlerts, MongoGuild
from fastapi import status, HTTPException

def generate_token():
  return secrets.token_urlsafe(32)

async def get_token_guild(db, token):
  docs = await db.get_document("servers", {"auth_key": token})
  if len(docs) == 0:
    return None

  doc = docs[0]
  doc.pop("_id", None)
  data = MongoGuild(**doc)
  return data

async def get_guild_alerts(db, guild_id):
  docs = await db.get_document("alerts", {"guild_id": guild_id})
  if len(docs) == 0:
    return None

  doc = docs[0]
  doc.pop("_id", None)
  data = MongoAlerts(**doc)
  return data

async def manage_alert(db, token, message):
  guild = await get_token_guild(db, token)
  if guild == None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Servidor no encontrado"
    )

  alerts = await get_guild_alerts(db, guild.id)
  if alerts == None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Servidor no encontrado"
    )

  print(message)
  print(guild)
  print(alerts)