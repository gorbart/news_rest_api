from datetime import datetime

from app.server.cruds.author import get_author
from app.server.models.article import ArticleModel


async def convert_to_standard_model(article):
    article = ArticleModel(**article).dict()
    article['_id'] = article.pop('id')
    return article


async def assign_author(article):
    author = await get_author(article['author'])
    article['author'] = author


async def convert_date(article):
    article['publication_time'] = datetime.strptime(article['publication_time'], '%Y-%m-%dT%H:%M')