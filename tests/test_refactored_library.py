import pytest
from models.book import Book
from models.library import Library
from pydantic import ValidationError
from pydantic_core import PydanticCustomError
from library_system.exceptions import EmptyError, StateError

@pytest.fixture()
def multiple_books() -> list[Book]:
    books = [
    Book(title="  The Hobbit  ", author=" J.R.R. Tolkien "),
    Book(title="1984", author="George Orwell", status="borrowed"),
    Book(title="To Kill a Mockingbird", author="Harper Lee"),
]
    return books

@pytest.fixture()
def library(multiple_books: list[Book]) -> Library:
    library = Library(inventory=multiple_books, borrow_records=[])
    return library



class TestLibray:
    def test_valid_library(self, library: Library):
        assert len(library.inventory) == 3
        assert library.borrow_records == []
        assert library.inventory[0].title == 'the hobbit'
        assert library.inventory[0].author == 'j.r.r. tolkien'
    
    def test_libray_edge_cases_scenarios(self):
        with pytest.raises(ValidationError) as exc_info:
            library = Library(inventory = [1,2,3], borrow_records=[1,2])

        errors = exc_info.value.errors()
        print("Validation Errors:")
        for error in errors:
            field = ".".join(str(loc) for loc in error['loc'])
            msg = error['msg']
            print(f"- Field: {field} → Error: {msg}")

        assert len(errors) == 5

    def test_inventory_with_duplicates(self, multiple_books : list[Book]):
        library = Library(inventory=[multiple_books[0], multiple_books[0], multiple_books[1]], borrow_records=[])
        assert len(library.inventory) == 2

    def test_add_book(self, library: Library):
       
        new_book = Book(title='this is us', author='zidane')
        library.add_book(book= new_book)
        assert len(library.inventory) == 4
        assert library.inventory[-1].title == 'this is us'
    
    def test_edge_cases_for_add_book(
            self,
            library: Library,
            multiple_books: Book):
        with pytest.raises(TypeError, match='Excpected Book object'):
            library.add_book('new book')

        with pytest.raises(PydanticCustomError, match='already exists in the inventory') as exc_info:
            library.add_book(book=multiple_books[0])

    def test_borrow_available_book_successfully(self, library: Library):
        library.borrow_book(borrower_name="Hasan", book_id=1)

        assert library.inventory[0].status == "borrowed"
        assert len(library.borrow_records) == 1
        assert library.borrow_records[0].borrower_name == "hasan"
        assert library.borrow_records[0].title == "the hobbit"
        assert library.borrow_records[0].return_time is None

    def test_borrow_already_borrowed_book_raises_error(self, library: Library):
        with pytest.raises(ValueError, match="already borrowed"):
            library.borrow_book(borrower_name="Hasan", book_id=2)

        assert len(library.borrow_records) == 0

    def test_borrow_book_with_non_int_id_raises_error(self, library: Library):
        with pytest.raises(ValueError, match="id must be int"):
            library.borrow_book(borrower_name="Hasan", book_id="1")

    def test_borrow_book_with_bool_id_raises_error(self, library: Library):
        with pytest.raises(ValueError, match="id must be int"):
            library.borrow_book(borrower_name="Hasan", book_id=True)

    def test_borrow_book_with_zero_id_raises_error(self, library: Library):
        with pytest.raises(ValueError, match="invalid id"):
            library.borrow_book(borrower_name="Hasan", book_id=0)

    def test_borrow_book_with_negative_id_raises_error(self, library: Library):
        with pytest.raises(ValueError, match="invalid id"):
            library.borrow_book(borrower_name="Hasan", book_id=-1)

    def test_borrow_book_with_out_of_range_id_raises_error(self, library: Library):
        with pytest.raises(ValueError, match="invalid id"):
            library.borrow_book(borrower_name="Hasan", book_id=99)

    def test_borrow_book_with_invalid_borrower_name_raises_validation_error(self, library: Library):
        with pytest.raises(ValidationError):
            library.borrow_book(borrower_name="ab", book_id=1)

    def test_borrowing_one_book_does_not_change_other_books(self, library: Library):
        library.borrow_book(borrower_name="Hasan", book_id=1)

        assert library.inventory[0].status == "borrowed"
        assert library.inventory[1].status == "borrowed"
        assert library.inventory[2].status == "available"

    def test_view_books(self, multiple_books: list[Book], capsys):
        Library.view_books(multiple_books)

        captured = capsys.readouterr()  
        assert "ID" in captured.out
        assert "Title" in captured.out
        assert "Author" in captured.out
        assert "Status" in captured.out

        assert "the hobbit" in captured.out
        assert "j.r.r. tolkien" in captured.out
        assert "1984" in captured.out
        assert "george orwell" in captured.out
        assert "Total books: 3" in captured.out

    def test_view_books_empty_list_raises_error(self):
        with pytest.raises(EmptyError, match="Book list is empty"):
            Library.view_books([])
    
    def test_view_available_books(self, library: Library, capsys):
        library.view_available_books()

        captured = capsys.readouterr()

        assert "Available Books" in captured.out
        assert "the hobbit" in captured.out
        assert "to kill a mockingbird" in captured.out
        assert "1984" not in captured.out
        assert "Total books: 2" in captured.out


    def test_view_available_books_when_no_available_books_raises_error(self, multiple_books: list[Book]):
        for book in multiple_books:
            book.status = "borrowed"

        library = Library(inventory=multiple_books, borrow_records=[])

        with pytest.raises(StateError, match="books are already borrowed"):
            library.view_available_books()

    def test_view_borrowed_books(self, library: Library, capsys):
        library.view_borrowed_books()

        captured = capsys.readouterr()

        assert "Borrowed Books" in captured.out
        assert "1984" in captured.out
        assert "george orwell" in captured.out
        assert "the hobbit" not in captured.out
        assert "to kill a mockingbird" not in captured.out
        assert "Total books: 1" in captured.out


    def test_view_borrowed_books_when_no_borrowed_books_raises_error(self, multiple_books: list[Book]):
        for book in multiple_books:
            book.status = "available"

        library = Library(inventory=multiple_books, borrow_records=[])

        with pytest.raises(StateError, match="All books are available"):
            library.view_borrowed_books()

    def test_return_book_successfully(self, library: Library):
        library.borrow_book(borrower_name="Hasan", book_id=1)

        result = library.return_book(record_id=1)

        assert result is True
        assert library.borrow_records[0].status == "returned"
        assert library.borrow_records[0].return_time is not None
        assert library.inventory[0].status == "available"


    def test_return_book_with_non_int_record_id_raises_error(self, library: Library):
        with pytest.raises(ValueError, match="id must be int"):
                library.return_book(record_id="1")


    def test_return_book_with_bool_record_id_raises_error(self, library: Library):
        with pytest.raises(ValueError, match="id must be int"):
            library.return_book(record_id=True)


    def test_return_book_with_zero_record_id_raises_error(self, library: Library):
        with pytest.raises(ValueError, match="invalid id"):
            library.return_book(record_id=0)


    def test_return_book_with_negative_record_id_raises_error(self, library: Library):
        with pytest.raises(ValueError, match="invalid id"):
            library.return_book(record_id=-1)


    def test_return_book_with_out_of_range_record_id_raises_error(self, library: Library):
        with pytest.raises(ValueError, match="invalid id"):
            library.return_book(record_id=99)


    def test_return_already_returned_book_raises_error(self, library: Library):
        library.borrow_book(borrower_name="Hasan", book_id=1)
        library.return_book(record_id=1)

        with pytest.raises(StateError, match="already returned"):
            library.return_book(record_id=1)


    def test_return_book_when_book_missing_from_inventory_raises_error(self, library: Library):
        library.borrow_book(borrower_name="Hasan", book_id=1)

        borrowed_book = library.inventory.pop(0)

        with pytest.raises(StateError, match="Borrowed book was not found in inventory"):
            library.return_book(record_id=1)

        




    
