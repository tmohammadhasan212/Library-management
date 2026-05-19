from pydantic import BaseModel, Field
from typing import Annotated, Literal

class Book(BaseModel):
    title : Annotated[str, Field(min_length=3)]
    uid : int | None = None
    author : Annotated[str, Field(min_length=3)]
    status : Literal['available', 'borrowed'] = 'available'