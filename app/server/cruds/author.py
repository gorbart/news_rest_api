from typing import List
from app.server.cruds.utils import get_entities, get_entity, add_entity, update_entity, delete_entity
from app.server.cruds.database import author_collection


# Get all the authors
async def get_authors() -> List[dict]:
    return await get_entities(author_collection)


# Get an author with a given id
async def get_author(author_id: str) -> dict:
    return await get_entity(author_collection, author_id)


# Add a new author with given data
async def add_author(author_data: dict) -> dict:
    return await add_entity(author_collection, author_data)


# Update an author with a given id
async def update_author(author_id: str, author_data: dict) -> bool:
    return await update_entity(author_collection, author_data, author_id)


# Delete an author with a given id
async def delete_author(author_id: str) -> bool:
    return await delete_entity(author_collection, author_id)
