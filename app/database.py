from motor.motor_asyncio import AsyncIOMotorClient
import aioredis
import os

MONGO_DETAILS = os.getenv("MONGO_URI", "mongodb://localhost:27017")

client = AsyncIOMotorClient(MONGO_DETAILS)

# Access the specific database (create one if it doesn’t exist)
database = client["paper_db"]

# Access the collection (like a table in SQL)
paper_collection = database["papers"]

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

redis = aioredis.from_url(REDIS_URL, decode_responses=True)
