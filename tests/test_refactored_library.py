import pytest
from models.book import Book
from models.library import Library
from pydantic import ValidationError
from pydantic_core import PydanticCustomError

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


        




    
