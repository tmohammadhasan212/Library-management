import pytest
from models.book import Book
from models.library import Library

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