import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel

from app.models.author import AuthorModel
from app.models.basemodels import DBModel


class ArticleModel(DBModel):
    title: str
    text: str
    publication_date: datetime.datetime
    source: str
    author: AuthorModel

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Poland wins the football World Cup!",
                "text": "Poland wins the football World Cup after a difficult game with England. Robert Lewandowski"
                        "scored both of Poland's goals.",
                "publication_date": datetime.datetime.now(),
                "source": "marca.com",
            }
        }


class UpdateArticleModel(BaseModel):
    title: Optional[str]
    text: Optional[str]
    publication_date: Optional[datetime.datetime]
    source: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Poland wins the football World Cup!",
                "text": "Poland wins the football World Cup after a difficult game with England. Robert Lewandowski"
                        "scored both of Poland's goals.",
                "publication_date": datetime.datetime.now(),
                "source": "marca.com",
            }
        }
