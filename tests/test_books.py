import pytest
from pydantic import ValidationError
from models.book import Book


class TestBook:
    def setup_method(self):
        Book.reset_counter()

    def test_create_valid_book_with_auto_uid(self):
        book = Book(title="The Hobbit", author="J.R.R. Tolkien")

        assert book.uid == 1
        assert book.title == "the hobbit"
        assert book.author == "j.r.r. tolkien"
        assert book.status == "available"

    def test_create_valid_book_with_manual_uid(self):
        book = Book(uid=10, title="1984", author="George Orwell")

        assert book.uid == 10
        assert Book.counter == 10

    def test_auto_uid_continues_after_manual_uid(self):
        Book(uid=5, title="1984", author="George Orwell")
        book = Book(title="Dune", author="Frank Herbert")

        assert book.uid == 6

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

    def test_uid_must_be_positive(self):
        with pytest.raises(ValidationError):
            Book(uid=0, title="1984", author="George Orwell")

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

    def test_multiple_books_get_incrementing_uids(self):
        book1 = Book(title="1984", author="George Orwell")
        book2 = Book(title="Dune", author="Frank Herbert")

        assert book1.uid == 1
        assert book2.uid == 2
    
    def test_manual_uid_lower_than_counter_does_not_reset_counter(self):
        Book(title="1984", author="George Orwell")  # uid = 1
        Book(uid=10, title="Dune", author="Frank Herbert")

        book = Book(uid=5, title="The Hobbit", author="J.R.R. Tolkien")
        next_book = Book(title="Foundation", author="Isaac Asimov")

        assert book.uid == 5
        assert next_book.uid == 11


    def test_uid_cannot_be_negative(self):
        with pytest.raises(ValidationError):
            Book(uid=-1, title="1984", author="George Orwell")


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