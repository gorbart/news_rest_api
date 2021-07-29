from typing import List

from bson import json_util
from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from app.server.cruds.author import add_author, get_authors, get_author, update_author, delete_author
from app.server.models.article import AuthorModel
from app.server.models.author import UpdateAuthorModel
from app.server.routes.utils import update_entity, get_update_results, convert_to_standard_model

AUTHOR_NOT_FOUND_MESSAGE = 'Author with id {} not found'

router = APIRouter()


@router.get('/', response_description='List all authors of articles', response_model=List[AuthorModel])
async def get_author_list() -> List[dict]:
    articles = await get_authors()
    return articles


@router.get('/{author_id}', response_description='Get an author with given id', response_model=AuthorModel)
async def get_one_author(author_id: str) -> dict:
    author = await get_author(author_id)
    if author is not None:
        return author

    raise HTTPException(status_code=404, detail=AUTHOR_NOT_FOUND_MESSAGE.format(author_id))


@router.post('/', response_description='Add new author to database', response_model=AuthorModel)
async def add_author_data(raw_author: AuthorModel = Body(...)) -> JSONResponse:
    raw_author = jsonable_encoder(raw_author)
    author = await convert_to_standard_model(raw_author, AuthorModel)
    new_author = await add_author(author)
    new_author = json_util.dumps(new_author)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_author)


@router.put('/{author_id}', response_description='Update an author in database', response_model=AuthorModel)
async def update_author_data(author_id: str, received_author_data: UpdateAuthorModel = Body(...)) -> JSONResponse:
    is_successful = await update_entity(author_id, received_author_data, update_author)

    author = await get_author(author_id)

    return await get_update_results(author, is_successful, AUTHOR_NOT_FOUND_MESSAGE.format(author_id))


@router.delete('/{author_id}', response_description='Delete an article from database')
async def delete_author_data(author_id: str) -> JSONResponse:
    if delete_author(author_id):
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=AUTHOR_NOT_FOUND_MESSAGE.format(author_id))
