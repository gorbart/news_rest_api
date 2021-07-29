from typing import List

from bson import json_util
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

from app.server.cruds.article import add_article, get_articles, get_article, update_article, delete_article
from app.server.models.article import CreateArticleModel, ArticleModel, UpdateArticleModel
from app.server.routes.utils import convert_date, assign_author, convert_to_standard_model

router = APIRouter()


@router.get('/', response_description='List all articles', response_model=List[ArticleModel])
async def get_article_list() -> List[dict]:
    articles = await get_articles()
    return articles


@router.get('/{article_id}', response_description='Get an article with given id', response_model=ArticleModel)
async def get_one_article(article_id: str) -> dict:
    if (article := await get_article(article_id)) is not None:
        return article

    raise HTTPException(status_code=404, detail=f'Article with id {article_id} not found')


@router.post('/', response_description='Add new article to database', response_model=ArticleModel)
async def add_article_data(raw_article: CreateArticleModel = Body(...)) -> JSONResponse:
    raw_article = jsonable_encoder(raw_article)
    await convert_date(raw_article)
    await assign_author(raw_article)
    article = await convert_to_standard_model(raw_article)
    new_article = await add_article(article)
    new_article = json_util.dumps(new_article)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_article)


@router.put('/{article_id}', response_description='Update an article in database', response_model=ArticleModel)
async def update_article_data(article_id: str, received_article_data: UpdateArticleModel = Body(...)) -> JSONResponse:
    new_article_data = {key: value for key, value in received_article_data.dict().items() if value is not None}

    is_successful = False

    if len(new_article_data) >= 1:
        is_successful = await update_article(article_id, new_article_data)

    article = await get_article(article_id)

    if article is not None:
        article = jsonable_encoder(article)
        if not is_successful:
            return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={'message': 'No changes occurred, '
                                                                                          'returning not changed '
                                                                                          'object', 'object': article})
        else:
            return JSONResponse(status_code=status.HTTP_200_OK, content=article)

    raise HTTPException(status_code=404, detail=f'Article with id {article_id} not found')


@router.delete('/{article_id}', response_description='Delete an article from database')
async def delete_article_data(article_id: str) -> JSONResponse:
    if delete_article(article_id):
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f'Article with id {id} not found')
