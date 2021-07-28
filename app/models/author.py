from typing import Optional

from bson import ObjectId
from pydantic import BaseModel

from app.models.basemodels import DBModel


class AuthorModel(DBModel):
    name: str
    surname: str
    website: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            'example': {
                'name': 'John',
                'surname': 'Doe',
                'website': 'johndoesportsjournalist.com'
            }
        }


class UpdateAuthorModel(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    website: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            'example': {
                'name': 'John',
                'surname': 'Doe',
                'website': 'johndoesportsjournalist.com'
            }
        }
