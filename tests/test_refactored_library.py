import pytest
from models.book import Book
from models.library import Library
from pydantic import ValidationError

@pytest.fixture()
def multiple_books() -> list[Book]:
    books = [
    Book(uid=1, title="  The Hobbit  ", author=" J.R.R. Tolkien "),
    Book(uid=2, title="1984", author="George Orwell", status="borrowed"),
    Book(uid=3, title="To Kill a Mockingbird", author="Harper Lee"),
]
    return books

class TestLibray:
    def test_valid_library(self, multiple_books):
        library = Library(inventory = multiple_books, borrow_records = [])
        assert len(library.inventory) == 3
        assert library.borrow_records == []
        assert library.inventory[0].uid == 1
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

    def test_inventory_with_duplicates(self, multiple_books):
        library = Library(inventory=[multiple_books[0], multiple_books[0], multiple_books[1]], borrow_records=[])
        assert len(library.inventory) == 2



    
