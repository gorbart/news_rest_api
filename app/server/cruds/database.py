import motor.motor_asyncio
from decouple import config

# Get configuration of MongoDB Atlas from .env file
MONGO_DETAILS = config('MONGO_DETAILS')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

news_db = client.news

# Assign collections to variables
article_collection = news_db['articles']
author_collection = news_db['authors']
