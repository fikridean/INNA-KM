from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DETAILS, DATABASE_NAME

try:
    client = AsyncIOMotorClient(MONGO_DETAILS)
    database = client[DATABASE_NAME]
    portal_collection = database.get_collection("portals")
    raw_collection = database.get_collection("raws")
    term_collection = database.get_collection("terms")
    taxon_collection = database.get_collection("taxa")

except Exception as e:
    raise ConnectionError(f"Could not connect to MongoDB: {str(e)}")
