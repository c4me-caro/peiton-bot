import secrets 
from db.objects import MongoAlerts, MongoGuild
from fastapi import status, HTTPException
import discord
import uuid

def generate_token():
  return secrets.token_urlsafe(32)

def generate_alert_id():
  return str(uuid.uuid4()).replace("-", "")

async def get_token_guild(db, token):
  docs = await db.get_document("servers", {"auth_key": token})
  if len(docs) == 0:
    return None

  doc = docs[0]
  doc.pop("_id", None)
  data = MongoGuild(**doc)
  return data

async def get_guild_alerts(db, guild_id, id):
  docs = await db.get_document("alerts", {"guild_id": guild_id, "id": id})
  if len(docs) == 0:
    return None

  doc = docs[0]
  doc.pop("_id", None)
  data = MongoAlerts(**doc)
  return data

async def retrieve_alert(channel, guild_name, guild_color, guild_icon, alert_title, alert_image_url, message):
  embed = discord.Embed(title=alert_title, color=guild_color if guild_color != 0 else 0)
  embed.set_footer(icon_url=guild_icon if guild_icon != "" else "", text=guild_name)

  if message != None:
    embed.add_field(name="Mensaje:", value=message, inline=True)

  if alert_image_url != "":
      embed.set_image(url=alert_image_url)

  await channel.send(embed=embed)

async def manage_alert(app, logger, token, id, message):
  guild = await get_token_guild(app.db, token)
  if guild == None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Servidor no encontrado"
    )

  alert = await get_guild_alerts(app.db, guild.id, id)
  if alert == None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Alerta no encontrada"
    )

  channel = app.get_channel(alert.channel) or await app.fetch_channel(alert.channel)
  if not channel:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, 
      detail="No se encontró el canal de Discord"
    )

  await retrieve_alert(channel, guild.name, guild.color, guild.icon, alert.title, alert.image_url, message)
  logger.log(f"Alerta generada en el servidor {guild.name}: {alert.id}")

async def validate_token(db, token, guild_id):
  guild = await get_token_guild(db, token)
  if guild == None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Servidor no encontrado"
    )

  return guild.id == guild_id