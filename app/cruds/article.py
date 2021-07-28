from typing import List

from app.cruds.database import article_collection
from app.cruds.utils import *


# Get all the articles
async def get_articles() -> List[dict]:
    return await get_entities(article_collection)


# Get an article with a given id
async def get_article(article_id: str) -> dict:
    return await get_entity(article_collection, article_id)


# Add a new article with given data
async def add_article(article_data: dict) -> dict:
    return await add_entity(article_collection, article_data)


# Update an article with a given id
async def update_article(article_id: str, article_data: dict) -> bool:
    return await update_entity(article_collection, article_data, article_id)


# Delete an article with a given id
async def delete_article(article_id: str) -> bool:
    return await delete_entity(article_collection, article_id)
