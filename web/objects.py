from pydantic import BaseModel

class Alerts(BaseModel):
  guild_id: int = 0
  title: str = ""
  image_url: str = ""
  channel: int = 0

class Welcome(BaseModel):
  guild_id: int = 0
  description: str = ""
  image_url: str = ""
  channel: int = 0