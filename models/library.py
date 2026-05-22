from pydantic import BaseModel, field_validator, ConfigDict
from .book import Book
from .borrow_record import BorrowRecord
from pydantic_core import PydanticCustomError
import time
from library_system.exceptions import EmptyError

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
    
    @staticmethod
    def view_books(books: list[Book]) -> None:
        if not books:
            raise EmptyError("Book list is empty.")

        print(f"{'ID':<5} {'Title':<30} {'Author':<25} {'Status':<12}")
        print("=" * 115)

        for index, book in enumerate(books, start=1):
            title = book.title[:27] + "..." if len(book.title) > 30 else book.title
            author = book.author[:22] + "..." if len(book.author) > 25 else book.author

            print(
                f"{index:<5} "
                f"{title:<30} "
                f"{author:<25} "
                f"{book.status:<12}"
            )

        print(f"\nTotal books: {len(books)}")
        
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

    def borrow_book(self, borrower_name: str, book_id: int) -> None:
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







