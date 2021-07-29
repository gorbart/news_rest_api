from typing import List

from bson import json_util
from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from app.server.cruds.article import add_article, get_articles, get_article, update_article, delete_article
from app.server.cruds.author import get_author
from app.server.models.article import CreateArticleModel, ArticleModel, UpdateArticleModel
from app.server.routes.utils import convert_date, convert_to_standard_model, update_entity, get_update_results

ARTICLE_NOT_FOUND_MESSAGE = 'Article with id {} not found'

router = APIRouter()


@router.get('/', response_description='List all articles', response_model=List[ArticleModel])
async def get_article_list() -> List[dict]:
    articles = await get_articles()
    return articles


@router.get('/{article_id}', response_description='Get an article with given id', response_model=ArticleModel)
async def get_one_article(article_id: str) -> dict:
    article = await get_article(article_id)
    if article is not None:
        return article

    raise HTTPException(status_code=404, detail=ARTICLE_NOT_FOUND_MESSAGE.format(article_id))


@router.post('/', response_description='Add new article to database', response_model=ArticleModel)
async def add_article_data(raw_article: CreateArticleModel = Body(...)) -> JSONResponse:
    raw_article = jsonable_encoder(raw_article)
    await convert_date(raw_article)
    await assign_author(raw_article)
    article = await convert_to_standard_model(raw_article, ArticleModel)
    new_article = await add_article(article)
    new_article = json_util.dumps(new_article)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_article)


@router.put('/{article_id}', response_description='Update an article in database', response_model=ArticleModel)
async def update_article_data(article_id: str, received_article_data: UpdateArticleModel = Body(...)) -> JSONResponse:
    is_successful = await update_entity(article_id, received_article_data, update_article)

    article = await get_article(article_id)

    return await get_update_results(article, is_successful, ARTICLE_NOT_FOUND_MESSAGE.format(article_id))


@router.delete('/{article_id}', response_description='Delete an article from database')
async def delete_article_data(article_id: str) -> JSONResponse:
    if await delete_article(article_id):
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=ARTICLE_NOT_FOUND_MESSAGE.format(article_id))


async def assign_author(article: dict) -> None:
    author = await get_author(article['author'])
    article['author'] = author
