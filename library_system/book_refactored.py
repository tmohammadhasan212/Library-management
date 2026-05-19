from pydantic import BaseModel, Field, model_validator, PositiveInt
from typing import Annotated, Literal

class Book(BaseModel):
    title : Annotated[str, Field(min_length=3)]
    uid : PositiveInt | None = None
    author : Annotated[str, Field(min_length=3)]
    status : Literal['available', 'borrowed'] = 'available'

    
class BookGenerator:
    __counter = 0
    def __init__(self, book: Book) -> None:
        self.book = self._validate_and_set_uid(book)

    def _validate_and_set_uid(self, book : Book) -> Book:
        if book.uid is None:
            BookGenerator.__counter += 1
            book.uid = BookGenerator.__counter
        else:
            if book.uid > BookGenerator.__counter:
                BookGenerator.__counter = book.uid
        return book
    

