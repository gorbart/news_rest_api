import motor.motor_asyncio
from decouple import config

MONGO_DETAILS = config('MONGO_DETAILS')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

news_db = client.news
authors_db = client.authors
