import pytest
from pydantic import ValidationError
from models.book import Book
from uuid import UUID, uuid4

class TestBook:
    
    def test_create_valid_book_with_auto_uid(self):
        book = Book(title="The Hobbit", author="J.R.R. Tolkien")

        assert type(book.uid) == UUID
        assert book.title == "the hobbit"
        assert book.author == "j.r.r. tolkien"
        assert book.status == "available"


    def test_status_can_be_borrowed(self):
        book = Book(title="Dune", author="Frank Herbert", status="borrowed")

        assert book.status == "borrowed"

    def test_invalid_status_raises_validation_error(self):
        with pytest.raises(ValidationError):
            Book(title="Dune", author="Frank Herbert", status="lost")

    def test_title_too_short_raises_validation_error(self):
        with pytest.raises(ValidationError):
            Book(title="ab", author="George Orwell")

    def test_author_too_short_raises_validation_error(self):
        with pytest.raises(ValidationError):
            Book(title="1984", author="ab")


    def test_strings_are_stripped_and_lowercased(self):
        book = Book(title="  The Hobbit  ", author="  J.R.R. Tolkien  ")

        assert book.title == "the hobbit"
        assert book.author == "j.r.r. tolkien"

    def test_assignment_validation_for_status(self):
        book = Book(title="1984", author="George Orwell")

        with pytest.raises(ValidationError):
            book.status = "missing"

    def test_assignment_validation_for_title_min_length(self):
        book = Book(title="1984", author="George Orwell")

        with pytest.raises(ValidationError):
            book.title = "ab"

    def test_missing_title_raises_validation_error(self):
        with pytest.raises(ValidationError):
            Book(author="George Orwell")


    def test_missing_author_raises_validation_error(self):
        with pytest.raises(ValidationError):
            Book(title="1984")


    def test_counter_is_not_in_model_dump(self):
        book = Book(title="1984", author="George Orwell")

        assert "counter" not in book.model_dump()


    def test_assignment_strips_and_lowercases_title(self):
        book = Book(title="1984", author="George Orwell")

        book.title = "  THE HOBBIT  "

        assert book.title == "the hobbit"


    def test_assignment_strips_and_lowercases_author(self):
        book = Book(title="1984", author="George Orwell")

        book.author = "  J.R.R. TOLKIEN  "

        assert book.author == "j.r.r. tolkien"