from datetime import datetime


async def convert_to_standard_model(entity, entity_class):
    entity = entity_class(**entity).dict()
    entity['_id'] = entity.pop('id')
    return entity


async def convert_date(entity):
    entity['publication_time'] = datetime.strptime(entity['publication_time'], '%Y-%m-%dT%H:%M')