from motor.motor_asyncio import AsyncIOMotorClient
from bot.logs import Logger
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, OperationFailure

log = Logger("database.log", 3)

class MongoController:
  def __init__(self, uri, db_name):
    try:
      self.client = AsyncIOMotorClient(uri)
      self.client.admin.command("ping")
      self.db = self.client[db_name]

      log.log("Conexión establecida con la base de datos")

    except ConnectionFailure:
      log.error("Ha fallado la conexión con la base de datos")

    except ServerSelectionTimeoutError:
      log.error("Ha fallado la conexión. El servidor no esta disponible")

    except Exception as e:
      log.error(str(e))

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