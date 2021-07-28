from typing import List

from bson import ObjectId


async def get_entities(collection) -> List[dict]:
    entities = [entity.dict() async for entity in collection.find()]
    return entities


async def get_entity(collection, entity_id: str) -> dict:
    entity = await collection.find_one({'_id': ObjectId(entity_id)})
    if entity:
        return entity.dict()


async def add_entity(collection, entity_data: dict) -> dict:
    entity = await collection.insert_one(entity_data)
    added_entity = await collection.find_one({'_id': entity.inserted_id})
    return added_entity.dict()


async def update_entity(collection, entity_data: dict, entity_id: str) -> bool:
    """Function returns False if request body is empty or entity with given id doesn't exist"""
    if len(entity_data) < 1:
        return False
    entity = await collection.find_one({"_id": ObjectId(entity_id)})
    if entity:
        updated_entity = await collection.update_one({"_id": ObjectId(entity_id)}, {"$set": entity_data})

        if updated_entity:
            return True
    return False


async def delete_entity(collection, entity_id: str) -> bool:
    """Function returns False if entity with given id doesn't exist"""
    entity = await collection.find_one({"_id": ObjectId(entity_id)})
    if entity:
        await collection.delete_one({"_id": ObjectId(entity_id)})
        return True
    return False
