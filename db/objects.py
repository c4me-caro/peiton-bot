from dataclasses import dataclass,asdict
from typing import Optional

@dataclass
class MongoGuild:
  id: int = 0
  name: str = ""
  icon: Optional[str] = None
  admin_role: str = "admin"
  color: int = 0
  auth_key: str = ""

  def to_dict(self):
    return asdict(self)

@dataclass
class MongoWelcome:
  guild_id: int = 0
  description: str = ""
  image_url: str = ""
  channel: str = ""
  color: int = 0

  def to_dict(self):
    return asdict(self)

@dataclass
class MongoAlerts:
  id: int = 0
  guild_id: int = 0
  title: str = ""
  channel: str = ""
  image_url: str = ""