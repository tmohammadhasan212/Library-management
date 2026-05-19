import pytest
from library_system.book_refactored import Book, BookGenerator

class TestBook:
    def setup_method(self):
        BookGenerator.reset_counter()

    def test_single_book_creation(self):
        book = Book(title="Harry Potter", author="J.K. Rowling")
        generator = BookGenerator(book)
        generated_book = generator.get_book()

        assert generated_book.uid == 1
        assert generated_book.title == "harry potter"
        assert generated_book.author == "j.k. rowling"
        assert generated_book.status == "available"