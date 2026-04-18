from motor.motor_asyncio import AsyncIOMotorClient
from bot.logs import Logger
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, OperationFailure

log = Logger("database.log", 3)

class MongoController:
  def __init__(self, uri, db_name):
    self.uri = uri
    self.db_name = db_name

  async def intialize_db(self):
    try:
      self.client = AsyncIOMotorClient(self.uri)
      self.client.admin.command("ping")
      self.db = self.client[self.db_name]

      log.log("Conexión establecida con la base de datos")
      return True
      
    except ConnectionFailure:
      log.error("Ha fallado la conexión con la base de datos")
      return False
    
    except ServerSelectionTimeoutError:
      log.error("Ha fallado la conexión. El servidor no esta disponible")
      return False
    
    except Exception as e:
      log.error(str(e))
      return False

  async def add_document(self, collection: str, data: dict):
    try:
      log.log(f"Registro insertado en {collection}: {str(data)}")
      result = await self.db[collection].insert_one(data)
      return result.inserted_id
    
    except OperationFailure as e:
      log.error(str(e))
      return None
    
  async def get_document(self, collection, filter={}):
    cursor = self.db[collection].find(filter)
    return await cursor.to_list(length=10)