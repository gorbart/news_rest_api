from typing import Callable

from bson import json_util
from fastapi import HTTPException
from pydantic import BaseModel
from starlette import status
from starlette.responses import JSONResponse

OBJECT_NOT_CHANGED_MESSAGE = 'No changes occurred, returning not changed object'


async def convert_to_standard_model(entity: dict, entity_class):
    entity = entity_class(**entity).dict()
    entity['_id'] = entity.pop('id')
    return entity


async def update_entity(entity_id: str, received_entity_data: BaseModel, update_function: Callable) -> bool:
    new_entity_data = {key: value for key, value in received_entity_data.dict().items() if value is not None}
    is_successful = False
    if len(new_entity_data) >= 1:
        is_successful = await update_function(entity_id, new_entity_data)
    return is_successful


async def get_update_results(entity: dict, is_successful: bool, fail_message: str) -> JSONResponse:
    if entity is not None:
        author = json_util.dumps(entity)
        if not is_successful:
            return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={'message': OBJECT_NOT_CHANGED_MESSAGE,
                                                                               'object': author})
        else:
            return JSONResponse(status_code=status.HTTP_200_OK, content=author)

    raise HTTPException(status_code=404, detail=fail_message)
