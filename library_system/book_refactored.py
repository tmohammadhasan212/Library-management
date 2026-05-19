from pydantic import BaseModel, Field, model_validator, PositiveInt, ConfigDict
from typing import Annotated, Literal

class Book(BaseModel):
    model_config = ConfigDict(validate_assignment=True, str_to_lower=True, str_strip_whitespace=True)
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
    
    def get_book(self) -> Book:
        return self.book
    
    @classmethod
    def reset_counter(cls) -> None:
        cls.__counter = 0

    @classmethod
    def generate_many(cls, list_of_books : list[Book]) -> list[Book]:
        result = []
        for book in list_of_books:
            if book.uid is None:
                cls.__counter += 1
                book.uid = cls.__counter
            else:
                if book.uid > cls.__counter:
                    cls.__counter = book.uid
            result.append(book)
        return result

    
