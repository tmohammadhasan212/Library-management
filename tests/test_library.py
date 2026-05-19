import pytest
from library_system.library import Library, Book
from library_system import exceptions
import time

# Test data
SAMPLE_BOOKS = [
    {"title": "Hamnet", "author": "Nolan"},
    {"title": "Little Woman", "author": "Debicki"},
    {"title": "Interstellar", "author": "Nolan"},
]

class TestLibrary:
    """Basic tests for Library class"""
    
    @pytest.fixture
    def empty_library(self):
        """Create an empty library"""
        Book.reset_counter()  # Reset book IDs
        return Library()
    
    @pytest.fixture
    def library_with_books(self):
        """Create a library with some books"""
        Book.reset_counter()
        lib = Library()
        lib.add_book("Hamnet", "Nolan")
        lib.add_book("Little Woman", "Debicki")
        lib.add_book("Interstellar", "Nolan", "borrowed")
        return lib

    # ========== TEST 1: Creating Library ==========
    
    def test_create_empty_library(self, empty_library):
        """Test that we can create an empty library"""
        assert empty_library.books == []
        assert empty_library.borrows_records == []
    
    def test_create_library_with_book_list(self):
        """Test creating library with a list of books"""
        Book.reset_counter()
        books = [
            Book("Hamnet", "Nolan"),
            Book("1984", "Orwell")
        ]
        lib = Library(books)
        assert len(lib.books) == 2
        assert lib.books[0].title == "Hamnet"
    
    def test_create_library_with_dict(self):
        """Test creating library with a dictionary"""
        Book.reset_counter()
        book_dict = {"title": "Hamnet", "author": "Nolan", "status": "available"}
        lib = Library(book_dict)
        assert len(lib.books) == 1
        assert lib.books[0].title == "Hamnet"

    # ========== TEST 2: Adding Books ==========
    
    def test_add_book(self, empty_library):
        """Test adding a book to library"""
        empty_library.add_book("Hamnet", "Nolan")
        assert len(empty_library.books) == 1
        assert empty_library.books[0].title == "Hamnet"
        assert empty_library.books[0].author == "Nolan"
        assert empty_library.books[0].status == "available"
    
    def test_add_book_with_custom_status(self, empty_library):
        """Test adding a book with custom status"""
        empty_library.add_book("Hamnet", "Nolan", "borrowed")
        assert empty_library.books[0].status == "borrowed"
    
    def test_add_duplicate_book_raises_error(self, empty_library):
        """Test that adding duplicate book raises StateError"""
        empty_library.add_book("Hamnet", "Nolan")
        
        with pytest.raises(exceptions.StateError, match="already exists"):
            empty_library.add_book("Hamnet", "Nolan")
    
    def test_add_book_obj(self, empty_library):
        """Test adding a Book object directly"""
        book = Book("Hamnet", "Nolan")
        empty_library.add_book_obj(book)
        assert len(empty_library.books) == 1
        assert empty_library.books[0] == book
    
    def test_add_invalid_book_obj_raises_error(self, empty_library):
        """Test adding non-Book object raises ValueError"""
        with pytest.raises(ValueError, match="Book instance"):
            empty_library.add_book_obj("not a book")

    # ========== TEST 3: Borrowing Books ==========
    
    def test_borrow_available_book(self, library_with_books):
        """Test borrowing an available book by ID"""
        # Book with ID 1 is 'Hamnet' (available)
        library_with_books.borrow_books("Hasan", 1)
        
        # Check book status changed
        assert library_with_books.books[0].status == "borrowed"
        
        # Check borrow record was created
        assert len(library_with_books.borrows_records) == 1
        assert library_with_books.borrows_records[0]["name"] == "Hasan"
        assert library_with_books.borrows_records[0]["book"].title == "Hamnet"
        assert library_with_books.borrows_records[0]["return_time"] is None
    
    def test_borrow_book_with_empty_name_raises_error(self, library_with_books):
        """Test that empty borrower name raises ValueError"""
        with pytest.raises(ValueError, match="Borrower name cannot be empty"):
            library_with_books.borrow_books("", 1)
        
        with pytest.raises(ValueError, match="Borrower name cannot be empty"):
            library_with_books.borrow_books("   ", 1)
    
    def test_borrow_book_from_empty_library_raises_error(self, empty_library):
        """Test borrowing from empty library raises EmptyError"""
        with pytest.raises(exceptions.EmptyError, match="Library is empty"):
            empty_library.borrow_books("Hasan", 1)
    
    def test_borrow_unavailable_book_raises_error(self, library_with_books):
        """Test borrowing a book that's already borrowed"""
        # Book with ID 3 is 'Interstellar' (already borrowed)
        with pytest.raises(exceptions.StateError, match="already been borrowed"):
            library_with_books.borrow_books("Hasan", 3)
    
    def test_borrow_nonexistent_book_raises_error(self, library_with_books):
        """Test borrowing a book with invalid ID"""
        with pytest.raises(ValueError, match="Invalid ID"):
            library_with_books.borrow_books("Hasan", 999)

    # ========== TEST 4: Returning Books ==========
    
    def test_return_borrowed_book(self, library_with_books):
        """Test returning a borrowed book"""
        # First borrow a book
        library_with_books.borrow_books("Hasan", 1)
        
        # Then return it
        result = library_with_books.return_book(1)
        
        assert result is True
        assert library_with_books.books[0].status == "available"
        assert library_with_books.borrows_records[0]["return_time"] is not None
    
    def test_return_book_not_borrowed_raises_error(self, library_with_books):
        """Test returning a book that wasn't borrowed"""
        with pytest.raises(exceptions.NotFoundError, match="No book with the book id"):
            library_with_books.return_book(1)

    # ========== TEST 5: Viewing Books ==========
    
    def test_view_books_prints_output(self, library_with_books, capsys):
        """Test that view_books prints book information"""
        library_with_books.view_books()
        captured = capsys.readouterr()
        
        assert "ID" in captured.out
        assert "Title" in captured.out
        assert "Hamnet" in captured.out
        assert "Nolan" in captured.out
    
    def test_view_books_empty_library_raises_error(self, empty_library):
        """Test viewing books from empty library raises error"""
        with pytest.raises(exceptions.EmptyError, match="Library is empty"):
            empty_library.view_books()
    
    def test_view_single_book(self, library_with_books):
        """Test viewing a single book"""
        book = library_with_books.books[0]
        library_with_books.view_books(book=book)
        # Just verify it doesn't raise error - we'll trust capsys for actual output
    
    def test_view_books_with_custom_list(self, library_with_books):
        """Test viewing a custom list of books"""
        available_books = [library_with_books.books[0]]
        library_with_books.view_books(book_list=available_books)
        # Verify doesn't raise error
    
    def test_view_books_with_both_parameters_raises_error(self, library_with_books):
        """Test that providing both book and book_list raises error"""
        book = library_with_books.books[0]
        book_list = [book]
        
        with pytest.raises(ValueError, match="Cannot specify both"):
            library_with_books.view_books(book=book, book_list=book_list)

    # ========== TEST 6: Available and Borrowed Books ==========
    
    def test_view_available_books(self, library_with_books, capsys):
        """Test viewing only available books"""
        library_with_books.view_available_books()
        captured = capsys.readouterr()
        
        assert "AVAILABLE BOOKS" in captured.out
        assert "Hamnet" in captured.out  # Available
        assert "Little Woman" in captured.out  # Available
        assert "Interstellar" not in captured.out  # Borrowed
    
    def test_view_available_books_when_none_available(self, library_with_books):
        """Test viewing available books when none are available"""
        # Borrow all available books
        library_with_books.borrow_books("Hasan", 1)
        library_with_books.borrow_books("Hasan", 2)
        
        with pytest.raises(exceptions.StateError, match="All books in the library"):
            library_with_books.view_available_books()
    
    def test_view_borrowed_books(self, library_with_books, capsys):
        """Test viewing only borrowed books"""
        library_with_books.view_borrowed_books()
        captured = capsys.readouterr()
        
        assert "BORROWED BOOKS" in captured.out
        assert "Interstellar" in captured.out  # Borrowed
    
    def test_view_borrowed_when_none_borrowed(self, empty_library):
        """Test viewing borrowed books when none are borrowed"""
        empty_library.add_book("Hamnet", "Nolan")
        
        with pytest.raises(exceptions.StateError, match="All books"):
            empty_library.view_borrowed_books()

    # ========== TEST 7: Sorting ==========
    
    def test_sort_books_by_id(self, empty_library):
        """Test sorting books by ID"""
        Book.reset_counter()
        
        # Add books out of order (using custom IDs)
        book3 = Book("Book3", "Author3", id=3)
        book1 = Book("Book1", "Author1", id=1)
        book2 = Book("Book2", "Author2", id=2)
        
        empty_library.add_book_obj(book3)
        empty_library.add_book_obj(book1)
        empty_library.add_book_obj(book2)
        
        sorted_books = empty_library.sort_books_by_id()
        
        assert sorted_books[0].id == 1
        assert sorted_books[1].id == 2
        assert sorted_books[2].id == 3

    # ========== TEST 8: Borrow History ==========
    
    def test_view_borrow_history(self, library_with_books, capsys):
        """Test viewing borrow history"""
        library_with_books.borrow_books("Hasan", 1)
        library_with_books.view_borrow_history()
        captured = capsys.readouterr()
        
        assert "BORROWING HISTORY" in captured.out
        assert "Hasan" in captured.out
    
    def test_view_borrow_history_for_specific_book(self, library_with_books, capsys):
        """Test viewing borrow history for a specific book"""
        library_with_books.borrow_books("Hasan", 1)
        book = library_with_books.books[0]
        library_with_books.view_borrow_history(book=book)
        captured = capsys.readouterr()
        assert "BORROWING HISTORY" in captured.out
    
    def test_view_borrow_history_for_unborrowed_book_raises_error(self, library_with_books):
        """Test viewing history for a book that was never borrowed"""
        book = library_with_books.books[2]  # This book is borrowed initially
        with pytest.raises(exceptions.NotFoundError, match="No borrowing records"):
            library_with_books.view_borrow_history(book=book)

    # ========== TEST 9: Convert to Dict ==========
    
    def test_to_dict(self, library_with_books):
        """Test converting books to dictionaries"""
        book_dicts = Library.to_dict(library_with_books.books)
        
        assert len(book_dicts) == 3
        assert book_dicts[0]["title"] == "Hamnet"
        assert book_dicts[0]["author"] == "Nolan"
        assert "id" in book_dicts[0]
        assert "status" in book_dicts[0]
    
    def test_to_dict_empty_list(self):
        """Test converting empty list to dict"""
        result = Library.to_dict([])
        assert result == []
    
    def test_convert_to_book_obj(self):
        """Test converting dict list to Book objects"""
        Book.reset_counter()
        books_dict = [
            {"id": 1, "title": "Hamnet", "author": "Nolan", "status": "available"},
            {"id": 2, "title": "1984", "author": "Orwell", "status": "borrowed"}
        ]
        
        books = Library.convert_to_book_obj(books_dict)
        
        assert len(books) == 2
        assert isinstance(books[0], Book)
        assert books[0].title == "Hamnet"
        assert books[1].status == "borrowed"

    # ========== TEST 10: Find Mismatches ==========
    
    def test_find_unmatched_books_no_mismatches(self, library_with_books):
        """Test finding mismatches when there are none"""
        # Convert library books to dict and back
        book_dicts = Library.to_dict(library_with_books.books)
        same_books = Library.convert_to_book_obj(book_dicts)
        
        mismatches = library_with_books.find_unmatched_books(same_books)
        assert mismatches == []
    
    def test_find_unmatched_books_with_mismatches(self, library_with_books):
        """Test finding mismatched books"""
        # Create a different version of a book
        different_books = [
            Book("Different Title", "Different Author", id=1)
        ]
        
        mismatches = library_with_books.find_unmatched_books(different_books)
        assert len(mismatches) > 0

    # ========== TEST 11: Edge Cases and Validation ==========
    
    def test_add_book_with_empty_title_raises_error(self, empty_library):
        """Test adding book with empty title"""
        with pytest.raises(ValueError, match="title can not be empty"):
            empty_library.add_book("", "Nolan")
    
    def test_add_book_with_empty_author_raises_error(self, empty_library):
        """Test adding book with empty author"""
        with pytest.raises(ValueError, match="author can not be empty"):
            empty_library.add_book("Hamnet", "")
    
    def test_case_insensitive_duplicate_check(self, empty_library):
        """Test that duplicate check is case-insensitive"""
        empty_library.add_book("hamnet", "nolan")
        
        with pytest.raises(exceptions.StateError, match="already exists"):
            empty_library.add_book("HAMNET", "NOLAN")

    def test_find_unmatched_borrows_no_mismatches(self, library_with_books):
        """Test when there are no mismatches between records"""
        # Borrow some books
        library_with_books.borrow_books("Hasan", 1)
        library_with_books.borrow_books("Ali", 2)
        
        # Create CSV records that match exactly
        csv_records = library_with_books.borrows_records.copy()
        
        # Should find no mismatches
        mismatches = library_with_books.find_unmatched_borrows(csv_records)
        
        assert mismatches == []
    
    def test_find_unmatched_borrows_extra_record_in_library(self, library_with_books):
        """Test when library has a record not in CSV"""
        # Borrow some books
        library_with_books.borrow_books("Hasan", 1)
        library_with_books.borrow_books("Ali", 2)
        
        # CSV missing the second record
        csv_records = [library_with_books.borrows_records[0]]  # Only first record
        
        mismatches = library_with_books.find_unmatched_borrows(csv_records)
        
        # Should find the record that's in library but not in CSV
        assert len(mismatches) == 1
        assert mismatches[0] == library_with_books.borrows_records[1]
    
    def test_find_unmatched_borrows_extra_record_in_csv(self, library_with_books, capsys):
        """Test when CSV has a record not in library"""
        # Borrow one book
        library_with_books.borrow_books("Hasan", 1)
        
        # Create CSV with an extra record
        csv_records = library_with_books.borrows_records.copy()
        
        # Add a fake record that's not in library
        fake_record = {
            'name': 'Fake User',
            'book': library_with_books.books[0],
            'borrow_time': 1234567890,
            'return_time': None
        }
        csv_records.append(fake_record)
        
        mismatches = library_with_books.find_unmatched_borrows(csv_records)
        
        # Should find the record that's in CSV but not in library
        assert len(mismatches) == 1
        assert mismatches[0] == fake_record
    
    def test_find_unmatched_borrows_multiple_mismatches(self, library_with_books):
        """Test when there are multiple mismatches on both sides"""
        # Borrow three books
        library_with_books.borrow_books("Hasan", 1)
        library_with_books.borrow_books("Ali", 2)
        
        # Create CSV with different records
        csv_records = [
            # Missing record 1 (index 1)
            library_with_books.borrows_records[0],  # Match
        ]
        
        # Add a fake record to CSV
        fake_record = {
            'name': 'Fake User',
            'book': library_with_books.books[0],
            'borrow_time': 1234567890,
            'return_time': None
        }
        csv_records.append(fake_record)
        
        mismatches = library_with_books.find_unmatched_borrows(csv_records)
        
        # Should find:
        # 1. Record in library but not in CSV (index 1)
        # 2. Fake record in CSV but not in library
        assert len(mismatches) == 2
        assert library_with_books.borrows_records[1] in mismatches
        assert fake_record in mismatches
    
    def test_find_unmatched_borrows_empty_library(self, empty_library):
        """Test when library has no borrow records"""
        # Empty CSV
        csv_records = []
        
        mismatches = empty_library.find_unmatched_borrows(csv_records)
        
        assert mismatches == []
    
    def test_find_unmatched_borrows_empty_csv(self, library_with_books):
        """Test when CSV is empty but library has records"""
        # Borrow a book
        library_with_books.borrow_books("Hasan", 1)
        
        csv_records = []
        
        mismatches = library_with_books.find_unmatched_borrows(csv_records)
        
        # Should find all library records as mismatches
        assert len(mismatches) == len(library_with_books.borrows_records)
        assert mismatches == library_with_books.borrows_records
    
    def test_find_unmatched_borrows_print_message(self, library_with_books, capsys):
        """Test that print message appears when there are mismatches"""
        # Borrow a book
        library_with_books.borrow_books("Hasan", 1)
        
        # Empty CSV (will cause mismatches)
        csv_records = []
        
        # Clear any existing output
        capsys.readouterr()
        
        mismatches = library_with_books.find_unmatched_borrows(csv_records)
        
        captured = capsys.readouterr()
        
        assert "There are some mismatches records" in captured.out
        assert len(mismatches) > 0
    
    def test_find_unmatched_borrows_no_print_when_no_mismatches(self, library_with_books, capsys):
        """Test that no print message appears when there are no mismatches"""
        # Borrow a book
        library_with_books.borrow_books("Hasan", 1)
        
        # CSV matches exactly
        csv_records = library_with_books.borrows_records.copy()
        
        # Clear any existing output
        capsys.readouterr()
        
        mismatches = library_with_books.find_unmatched_borrows(csv_records)
        
        captured = capsys.readouterr()
        
        assert "There are some mismatches records" not in captured.out
        assert mismatches == []
    
    def test_find_unmatched_borrows_with_different_order(self, library_with_books):
        """Test that order doesn't matter (records are compared by equality, not position)"""
        # Borrow books
        library_with_books.borrow_books("Hasan", 1)
        library_with_books.borrow_books("Ali", 2)
        
        # Create CSV with same records but different order
        csv_records = [
            library_with_books.borrows_records[1],  # Second record first
            library_with_books.borrows_records[0],  # First record second
        ]
        
        mismatches = library_with_books.find_unmatched_borrows(csv_records)
        
        # Should find no mismatches because sets are equal
        assert mismatches == []
    
    def test_find_unmatched_borrows_with_modified_record(self, library_with_books):
        """Test when CSV has a modified version of a record"""
        # Borrow a book
        library_with_books.borrow_books("Hasan", 1)
        
        # Create CSV with modified record (different name)
        modified_record = library_with_books.borrows_records[0].copy()
        modified_record['name'] = 'Different Name'
        
        csv_records = [modified_record]
        
        mismatches = library_with_books.find_unmatched_borrows(csv_records)
        
        # Both records are different, so both become mismatches
        assert len(mismatches) == 2
        assert library_with_books.borrows_records[0] in mismatches
        assert modified_record in mismatches