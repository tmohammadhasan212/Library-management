from pydantic import BaseModel, Field, PositiveInt, ConfigDict
from typing import Annotated, Literal

class Book(BaseModel):
    model_config = ConfigDict(validate_assignment=True, str_to_lower=True, str_strip_whitespace=True)
    title : Annotated[str, Field(min_length=3)]
    uid : PositiveInt | None = None
    author : Annotated[str, Field(min_length=3)]
    status : Literal['available', 'borrowed'] = 'available'