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
    
    def test_book_with_existing_uid(self):
        book = Book(title="1984", author="George Orwell", uid=5)
        generator = BookGenerator(book)
        assert generator.get_book().uid == 5

        new_book = Book(title="Dune", author="Frank Herbert")
        new_gen = BookGenerator(new_book)
        assert new_gen.get_book().uid == 6  # Counter incremented correctly

    def test_generate_many_books(self):
        books = [
            Book(title="Book One", author="Author A"),
            Book(title="Book Two", author="Author B"),
            Book(title="Book Three", author="Author C")
        ]
        generated_books = BookGenerator.generate_many(books)

        assert [b.uid for b in generated_books] == [1, 2, 3]
        # Check lowercasing
        assert generated_books[0].title == "book one"
        assert generated_books[1].author == "author b"