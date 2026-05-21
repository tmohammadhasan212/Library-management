from pydantic import BaseModel, Field, PositiveInt, ConfigDict, model_validator
from typing import Annotated, Literal, ClassVar
from uuid import UUID, uuid4

class Book(BaseModel):
    model_config = ConfigDict(validate_assignment=True, str_to_lower=True, str_strip_whitespace=True)
    title : Annotated[str, Field(min_length=3)]
    uid : UUID = Field(default_factory=uuid4)
    author : Annotated[str, Field(min_length=3)]
    status : Literal['available', 'borrowed'] = 'available'    