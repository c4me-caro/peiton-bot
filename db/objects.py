from dataclasses import dataclass,asdict

@dataclass
class MongoGuild:
  id: int = 0
  name: str = ""
  icon: str = ""
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
  channel: int = 0

  def to_dict(self):
    return asdict(self)

@dataclass
class MongoAlerts:
  id: str = ""
  guild_id: int = 0
  title: str = ""
  image_url: str = ""
  channel: int = 0

  def to_dict(self):
    return asdict(self)

@dataclass
class VoiceRooms:
  guild_id: int = 0
  channel: int = 0

  def to_dict(self):
    return asdict(self)