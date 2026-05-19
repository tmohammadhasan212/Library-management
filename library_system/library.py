from library_system.book import Book
from library_system.exceptions import *
import time
from typing import TypedDict, Literal

class BorrowRecord(TypedDict):
    """Represents a book borrowing record.
    
    Attributes:
        name: Name of the borrower
        book: The Book object being borrowed
        borrow_time: Timestamp when book was borrowed
        return_time: Timestamp when book was returned (None if still borrowed)
    """
    name: str
    book: Book
    borrow_time: float
    return_time: float | None

class BookDict(TypedDict):
    """Dictionary representation of a Book for serialization.
    
    Attributes:
        id: Unique identifier for the book
        title: Book title
        author: Book author name
        status: Current availability status ('borrowed' or 'available')
    """
    id: int
    title: str
    author: str
    status: Literal['borrowed', 'available']


class Library:
    """A library management system for tracking books and borrowing records.
    
    This class handles book inventory, borrowing/returning operations,
    and maintains borrowing history.
    
    Attributes:
        books: List of Book objects in the library
        borrows_records: List of BorrowRecord objects tracking all borrow operations
    
    Example:
        >>> library = Library()
        >>> library.add_book("1984", "George Orwell")
        >>> library.borrow_books("John Doe", 1)
    """
    
    def __init__(self, books: list[Book | BookDict] | BookDict | None = None) -> None:
        """Initialize the library with optional initial books.
        
        Args:
            books: Can be one of:
                - None: Start with empty library
                - BookDict: Single book as dictionary
                - list[Book]: List of Book objects
                - list[BookDict]: List of book dictionaries
        
        Example:
            >>> library = Library()  # Empty library
            >>> library = Library({'title': '1984', 'author': 'Orwell', 'status': 'available', 'id': 1})
        """
        self.books: list[Book] = []
        self.borrows_records: list[BorrowRecord] = []
        if books:
            if isinstance(books, dict):
                self.add_book(title=books['title'], author=books['author'], status=books['status'], id=books['id'])
            elif isinstance(books, list):
                for book in books:
                    if isinstance(book, Book):
                        self.add_book_obj(book)
                    else:
                        self.add_book(title=book['title'], author=book['author'], status=book['status'])
    
    def __validate_book_duplicate(self, title: str, author: str) -> bool:
        """Check if a book with same title and author already exists.
        
        Args:
            title: Book title to check
            author: Book author to check
            
        Returns:
            True if book doesn't exist (no duplicate)
            
        Raises:
            StateError: If a book with same title and author already exists
            
        Note:
            Comparison is case-insensitive
        """
        for book in self.books:
            if title.lower() == book.title.lower() and author.lower() == book.author.lower():
                raise StateError(f'Book "{title}" by {author} already exists in the system')
        return True
    
    def sort_books_by_id(self) -> list[Book]:
        """Return a sorted list of books by their ID.
        
        Returns:
            New list of Book objects sorted by ID in ascending order
            
        Example:
            >>> library.sort_books_by_id()
            [Book(id=1, title='1984'), Book(id=2, title='Brave New World')]
        """
        return sorted(self.books, key=lambda book: int(book.id))
    
    def add_book(
            self, title: str, author: str, status: Literal['available','borrowed'] = 'available', id: int | None = None) -> None:
        """Add a new book to the library.
        
        Args:
            title: Book title
            author: Book author
            status: Initial status ('available' or 'borrowed'). Defaults to 'available'
            id: Optional book ID. Auto-generated if not provided
            
        Raises:
            StateError: If a book with same title and author already exists
            
        Example:
            >>> library.add_book("The Hobbit", "J.R.R. Tolkien")
            >>> library.add_book("Dune", "Frank Herbert", id=100)
        """
        self.__validate_book_duplicate(title, author)
        book = Book(title, author, status, id)
        self.books.append(book)

    def add_book_obj(self, book: Book) -> None:
        """Add an existing Book object to the library.
        
        Args:
            book: Book instance to add
            
        Raises:
            ValueError: If provided argument is not a Book instance
            StateError: If duplicate book exists
            
        Example:
            >>> from library_system.book import Book
            >>> book = Book("Foundation", "Isaac Asimov")
            >>> library.add_book_obj(book)
        """
        if not isinstance(book, Book):
            raise ValueError('a Book instance need to be provided.')
        self.__validate_book_duplicate(title=book.title, author=book.author)
        self.books.append(book)

    def _check_book_availability(self, book: Book) -> bool:
        """Check if a specific book is available to borrow.
        
        Args:
            book: Book object to check
            
        Returns:
            True if book exists and is available
            
        Raises:
            StateError: If book exists but is already borrowed
            NotFoundError: If book doesn't exist in library
            
        Note:
            Internal method used by borrow_books()
        """
        if book in self.books:
            if book.status == 'available':
                return True
            raise StateError(f'The book with the title {book.title} has already been borrowed.')
        raise NotFoundError(f'There is no book called {book.title} in the system')
    
    def borrow_books(self, borrower_name: str, book_id: int) -> None:
        """Borrow a book from the library by its ID.
        
        Args:
            borrower_name: Name of person borrowing the book
            book_id: ID of the book to borrow
            
        Raises:
            ValueError: If borrower name is empty or book ID doesn't exist
            EmptyError: If library has no books
            StateError: If book is already borrowed
            
        Example:
            >>> library.add_book("1984", "Orwell", id=1)
            >>> library.borrow_books("John Doe", 1)
            The book "1984" has been successfully borrowed by John Doe at Mon Jan 1 12:00:00 2024
            
        Note:
            Creates a BorrowRecord and updates book status to 'borrowed'
        """
        # Validate borrower name
        if not borrower_name or not borrower_name.strip():
            raise ValueError('Borrower name cannot be empty')
    
        # Check if library has books
        if not self.books:
            raise EmptyError('Library is empty. Add some books first.')
    
        # Search for the book by ID
        for one_book in self.books:
            if one_book.id == book_id:
                self._check_book_availability(one_book)
                borrowed_time = time.time()
                one_book.status = 'borrowed'
                print(f'The book "{one_book.title}" has been successfully borrowed by {borrower_name} at {time.ctime(borrowed_time)}')
                borrow_record: BorrowRecord = {'name': borrower_name, 'book': one_book, 'borrow_time': borrowed_time, 'return_time': None}
                self.borrows_records.append(borrow_record)
                return
    
        raise ValueError(f'Invalid ID: {book_id}. No book exists with this ID.')
    
    def view_books(self, book: Book | None = None, book_list: list | None = None) -> None:
        """Display books in a formatted table.
        
        Args:
            book: Specific Book object to display (optional)
            book_list: List of books to display (optional)
            
        Raises:
            ValueError: If both book and book_list are provided
            EmptyError: If no books to display
            
        Note:
            Exactly one of book or book_list should be provided.
            If neither is provided, displays all books in library.
            
        Example:
            >>> library.view_books()  # Show all books
            >>> library.view_books(book=some_book)  # Show specific book
            >>> library.view_books(book_list=available_books)  # Show list of books
        """
        def print_row(id, title, author, status):
            new_title = (title[:27] + '...') if len(title) > 30 else title
            new_author = (author[:22] + '...') if len(author) > 25 else author
            print(f"{id:<5} {new_title:<30} {new_author:<25} {status:<12}")

        print(f"{'ID':<5} {'Title':<30} {'Author':<25} {'Status':<12}")
        print("=" * 75)

        if book and book_list is None:
            print_row(book.id, book.title, book.author, book.status)
        elif book is None and book_list is not None:
            if not book_list:
                raise EmptyError('The list of books is empty.')
            for one_book in book_list:
                print_row(one_book.id, one_book.title, one_book.author, one_book.status)
            print(f'\nTotal books: {len(book_list)}')
        elif book is None and book_list is None:
            if self.books:
                for one_book in self.books:
                    print_row(one_book.id, one_book.title, one_book.author, one_book.status)
                print(f'\nTotal books: {len(self.books)}')
            else:
                raise EmptyError('Library is empty. add some books first.')
        else:
            raise ValueError("Cannot specify both 'book' and 'book_list'")
    
    def view_available_books(self) -> None:
        """Display all books that are currently available to borrow.
        
        Raises:
            EmptyError: If library has no books
            StateError: If all books are borrowed
            
        Example:
            >>> library.view_available_books()
            📚 AVAILABLE BOOKS
            ID    Title                          Author                   Status
            ===========================================================================
            1     1984                           Orwell                   available
        """
        available_books = [book for book in self.books if book.status == 'available']
        if not available_books:
            if not self.books:
                raise EmptyError('Library is empty. add some books first.')
            raise StateError('All books in the library have been borrowed.')
        print('\n📚 AVAILABLE BOOKS\n')
        self.view_books(book_list=available_books)

    def view_borrowed_books(self) -> None:
        """Display all books that are currently borrowed.
        
        Raises:
            EmptyError: If library has no books
            StateError: If no books are borrowed (all available)
            
        Example:
            >>> library.view_borrowed_books()
            📚 BORROWED BOOKS
            ID    Title                          Author                   Status
            ===========================================================================
            1     1984                           Orwell                   borrowed
        """
        borrowed_books = [book for book in self.books if book.status == 'borrowed']
        if not borrowed_books:
            if not self.books:
                raise EmptyError('Library is empty. add some books first.')
            raise StateError('All books in the library are available.')
        print('\n📚 BORROWED BOOKS\n')
        self.view_books(book_list=borrowed_books)

    def return_book(self, book_id: int) -> bool:
        """Return a borrowed book to the library.
        
        Args:
            book_id: ID of the book to return
            
        Returns:
            True if book was successfully returned
            
        Raises:
            NotFoundError: If no borrowing record exists for this book
            
        Example:
            >>> library.return_book(1)
            The book with the title "1984" has been successfully returned.
            True
            
        Note:
            Updates book status to 'available' and sets return_time in record
        """
        for index, record in enumerate(self.borrows_records):
            if record['book'].id == book_id:
                print(f'The book with the title {record["book"].title} has been successfully returned.')
                record['return_time'] = time.time()
                record['book'].status = 'available'
                return True
        raise NotFoundError(f'No book with the book id : {book_id} is in the borrows records.')
    
    def view_borrow_history(self, book: Book | None = None) -> None:
        """Display borrowing history for all books or a specific book.
        
        Args:
            book: Optional specific book to show history for
            
        Raises:
            NotFoundError: If no records found for specified book
            
        Example:
            >>> library.view_borrow_history()  # Show all borrowing history
            >>> library.view_borrow_history(book=some_book)  # Show history for one book
        """
        def print_records(books):
            print(f"\n{'='*120}")
            print("BORROWING HISTORY".center(120))
            print(f"{'='*120}")
            print(f"{'Borrower':<20} {'Book':<20} {'Borrowed Time':<40} {'Return Time':<25} {'Status':<15}")
            print(f"{'-'*120}")
            for record in books:
                borrow_time_str = time.ctime(record['borrow_time'])
                return_time_str = time.ctime(record['return_time']) if record['return_time'] else "None"
                status = "RETURNED" if record['return_time'] else "BORROWED"
                print(f"{record['name']:<20} {record['book'].title:<20} {borrow_time_str:<40} {return_time_str:<25} {status:<15}")
            print(f"{'='*120}\n")

        if book is not None:
            books_to_print = [record for record in self.borrows_records if record['book'].title == book.title]
            if books_to_print:
                print(f"\n{'='*120}")
                print(f"BORROWING HISTORY for {book.title.upper()}".center(110))
                print_records(books_to_print)
            else:
                raise NotFoundError(f"No borrowing records found for book: {book.title}")
        else:
            print_records(self.borrows_records)

    @staticmethod
    def to_dict(books_list: list[Book]) -> list[BookDict]:
        """Convert a list of Book objects to dictionary format.
        
        Args:
            books_list: List of Book objects to convert
            
        Returns:
            List of BookDict dictionaries suitable for JSON serialization
            
        Example:
            >>> books_dict = Library.to_dict(library.books)
            >>> import json
            >>> json.dumps(books_dict)  # Can be saved to JSON file
        """
        books_as_dicts = []
        if books_list:
            for book in books_list:
                book_dict: BookDict = {'id': book.id, 'title': book.title, 'author': book.author, 'status': book.status}
                books_as_dicts.append(book_dict)
        return books_as_dicts
    
    @staticmethod
    def convert_to_book_obj(books: list[BookDict]) -> list[Book]:
        """Convert a list of book dictionaries back to Book objects.
        
        Args:
            books: List of BookDict dictionaries to convert
            
        Returns:
            List of Book objects
            
        Example:
            >>> from library_system.book import Book
            >>> books_data = [{'id': 1, 'title': '1984', 'author': 'Orwell', 'status': 'available'}]
            >>> books = Library.convert_to_book_obj(books_data)
        """
        new_books = []
        for one_book in books:
            book = Book(title=one_book['title'], author=one_book['author'], status=one_book['status'], id=int(one_book['id']))
            new_books.append(book)
        return new_books
    
    def find_unmatched_books(self, data_from_json: list[Book]) -> list[Book | None]:
        """Find books that exist in one collection but not the other.
        
        Args:
            data_from_json: List of Book objects from JSON source
            
        Returns:
            List of books that are mismatched (present in only one collection)
            or have differing data between collections
            
        Note:
            Compares library books with JSON-loaded books by ID.
            Returns books that are missing from either collection or have conflicts.
            
        Example:
            >>> json_books = load_books_from_json()
            >>> mismatches = library.find_unmatched_books(json_books)
            >>> if mismatches:
            ...     print(f"Found {len(mismatches)} books that need attention")
        """
        mismatches = []
        dict_lib = {book.id: book for book in self.books}
        dict_json = {book.id: book for book in data_from_json}
        all_ids = set(dict_lib.keys()) | set(dict_json.keys())

        for book_id in all_ids:
            lib_book = dict_lib.get(book_id)
            json_book = dict_json.get(book_id)

            if lib_book is None or json_book is None:
                mismatches.append(lib_book or json_book)
            elif lib_book != json_book:
                mismatches.append(json_book)

        if mismatches:
            print('There are some mismatches books between your library and the books you fetched from json file')
        return mismatches
    
    def find_unmatched_borrows(self, records_from_csv: list[BorrowRecord]) -> list[BorrowRecord]:
        """Find borrowing records that exist in one collection but not the other.
        
        Args:
            records_from_csv: List of BorrowRecord objects from CSV source
            
        Returns:
            List of records that are mismatched (present in library but not CSV,
            or in CSV but not library)
            
        Example:
            >>> csv_records = load_records_from_csv()
            >>> mismatches = library.find_unmatched_borrows(csv_records)
            >>> if mismatches:
            ...     print(f"Found {len(mismatches)} mismatched borrowing records")
        """
        mismatches = []
        for record in self.borrows_records:
            if record not in records_from_csv:
                mismatches.append(record)
        for record in records_from_csv:
            if record not in self.borrows_records:
                mismatches.append(record)
        if mismatches:
            print('There are some mismatches records between your library and the records you fetched from csv file')
        return mismatches


if __name__ == '__main__':
    print('hi')