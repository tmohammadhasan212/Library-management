import pytest
from models.book import Book
from models.library import Library
from pydantic import ValidationError
from pydantic_core import PydanticCustomError

@pytest.fixture()
def multiple_books() -> list[Book]:
    books = [
    Book(uid=1, title="  The Hobbit  ", author=" J.R.R. Tolkien "),
    Book(uid=2, title="1984", author="George Orwell", status="borrowed"),
    Book(uid=3, title="To Kill a Mockingbird", author="Harper Lee"),
]
    return books

@pytest.fixture()
def one_library_with_multiple_books(multiple_books: list[Book]) -> Library:
    library = Library(inventory=multiple_books, borrow_records=[])
    return library



class TestLibray:
    def test_valid_library(self, one_library_with_multiple_books: Library):
        assert len(one_library_with_multiple_books.inventory) == 3
        assert one_library_with_multiple_books.borrow_records == []
        assert one_library_with_multiple_books.inventory[0].uid == 1
        assert one_library_with_multiple_books.inventory[0].title == 'the hobbit'
        assert one_library_with_multiple_books.inventory[0].author == 'j.r.r. tolkien'
    
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

    def test_add_book(self, one_library_with_multiple_books: Library):
       
        new_book = Book(title='this is us', author='zidane')
        one_library_with_multiple_books.add_book(book= new_book)
        assert len(one_library_with_multiple_books.inventory) == 4
        assert one_library_with_multiple_books.inventory[-1].title == 'this is us'
    
    def test_edge_cases_for_add_book(
            self,
            one_library_with_multiple_books: Library,
            multiple_books: Book):
        with pytest.raises(TypeError, match='Excpected Book object'):
            one_library_with_multiple_books.add_book('new book')

        with pytest.raises(PydanticCustomError, match='already exists in the inventory') as exc_info:
            one_library_with_multiple_books.add_book(book=multiple_books[0])


        




    
