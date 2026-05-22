from pydantic import BaseModel, field_validator, ConfigDict
from .book import Book
from .borrow_record import BorrowRecord
from pydantic_core import PydanticCustomError
import time
from library_system.exceptions import EmptyError, StateError

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
            book_uid= book.uid,
            borrower_name=borrower_name,
            title=book.title,
            borrow_time=time.time()
        )

        book.status = 'borrowed'
        self.borrow_records.append(borrow_record)

    def view_available_books(self) -> None:
        available_books = [book for book in self.inventory if book.status == 'available']
        print("\nAvailable Books")
        print("=" * 40)
        if available_books:
            self.view_books(books=available_books)
        else:
            raise StateError('All books are already borrowed.')
        
    def view_borrowed_books(self) -> None:
        borrowed_books = [book for book in self.inventory if book.status == 'borrowed']
        print("\nBorrowed Books")
        print("=" * 40)
        if borrowed_books:
            self.view_books(books=borrowed_books)
        else:
            raise StateError('All books are available.')
        
    def return_book(self, record_id: int):
        if type(record_id) is not int:
            raise ValueError(f'id must be int. got {type(record_id).__name__}')

        if record_id < 1 or record_id > len(self.borrow_records):
            raise ValueError('invalid id. make sure it is in range.')
        
        looking_record = self.borrow_records[record_id - 1]
        if looking_record.status == 'returned':
            raise StateError(f"The Book with id {record_id} is already returned.")
        looking_record.status = 'returned'
        looking_record.return_time = time.time()

        # The status of the book in the inventory must be changed to "available"
        for book in self.inventory:
            if book.uid == looking_record.book_uid and book.status == 'borrowed':
                book.status = 'available'
                return True
        raise StateError("Borrowed book was not found in inventory.")










