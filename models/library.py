from pydantic import BaseModel, field_validator, ConfigDict
from .book import Book
from .borrow_record import BorrowRecord
from pydantic_core import PydanticCustomError
import time

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
    
    def add_book(self, book: Book) -> None:
        if not isinstance(book, Book):
            raise TypeError(f'Excpected Book object. got {type(book).__name__}')
        if book in self.inventory:
            raise PydanticCustomError(
                'book_already_exists',
                'The book {book_name} already exists in the inventory',
                {'book_name':book.title}
            )
        self.inventory.append(book)

    def borrow_book(self, borrower_name: str, book_id: int):
        if type(book_id) is not int:
            raise ValueError(f'id must be int. got {type(book_id).__name__}')

        if book_id < 1 or book_id > len(self.inventory):
            raise ValueError('invalid id. make sure it is in range.')

        book = self.inventory[book_id - 1]

        if book.status != 'available':
            raise ValueError(f'The book with id {book_id} is already borrowed.')

        borrow_record = BorrowRecord(
            borrower_name=borrower_name,
            title=book.title,
            borrow_time=time.time()
        )

        book.status = 'borrowed'
        self.borrow_records.append(borrow_record)
            






