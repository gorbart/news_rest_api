from bson import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    """
    Class PyObjectId maps MongoDB BSON id to JSON format, which is used by FastAPI.
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class DBModel(BaseModel):
    """DBModel class has id attribute which is a common attribute for all models being saved into database. It's
    automatically assigned to a model on its creation"""

    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
