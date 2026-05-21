from pydantic import BaseModel, field_validator, ConfigDict
from .book import Book
from .borrow_record import BorrowRecord
from pydantic_core import PydanticCustomError

class Library(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    inventory : list[Book]
    borrow_records : list[BorrowRecord]

    @field_validator('inventory', 'borrow_records')
    @classmethod
    def remove_duplicates(cls, value: list[Book | BorrowRecord]) -> list[Book | BorrowRecord]:
        seen = set()
        uniques = []
        for index, row in enumerate(value):
            uid = getattr(row, 'uid', None)
            if uid not in seen:
                seen.add(uid)
                uniques.append(row)
        return uniques


