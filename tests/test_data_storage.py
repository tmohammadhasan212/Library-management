import pytest
from models.library import Library
from models.book import Book
from models.borrow_record import BorrowRecord
from library_system.data_storage import DataStorage
from pathlib import Path
from library_system.exceptions import EmptyError
from pydantic import ValidationError

class TestCSVfiles:
    def test_dir_path_creation(self, tmp_path: Path):
        storage = DataStorage(dir_path= tmp_path)
        assert storage.dir_path.exists()
        assert storage.dir_path.is_dir()
        assert storage.dir_path == tmp_path.resolve()

    def test_export_borrow_records_to_csv(self, tmp_path: Path, library: Library):
        storage = DataStorage(dir_path= tmp_path)
        library.borrow_book(borrower_name='mohammad', book_id=1)
        result = storage.export_to_csv(library.borrow_records)
        file_path = tmp_path/ 'borrow_records.csv'
        assert file_path.exists()
        assert file_path.is_file()
        assert result is True
        assert 'mohammad' in file_path.read_text(encoding='utf-8')
        assert 'uid' in file_path.read_text(encoding='utf-8')

    def test_export_csv_with_invalid_data_list(self, tmp_path: Path, library: Library):
        storage = DataStorage(dir_path= tmp_path)
        library.borrow_book(borrower_name='mohammad', book_id=1)
        with pytest.raises(TypeError, match='must be BorrowRecord objects'):
            result = storage.export_to_csv(data= [library.borrow_records[0], 'not a BorrowRecord instance'])
        with pytest.raises(TypeError, match="data should be a list"):
            result = storage.export_to_csv(data= 'not a list')

    def test_import_from_csv(self, tmp_path: Path, library:Library):
        storage = DataStorage(dir_path= tmp_path)
        library.borrow_book(borrower_name= 'hasan', book_id= 1)
        storage.export_to_csv(data= library.borrow_records)
        data_from_csv = storage.import_from_csv()
        file_path = tmp_path / 'borrow_records.csv'

        assert isinstance(data_from_csv, list)
        assert isinstance(data_from_csv[0], BorrowRecord)
        assert file_path.is_file()
        assert data_from_csv[0].borrower_name == 'hasan'

    def test_import_csv_when_file_path_not_exist(self, tmp_path: Path):
        storage = DataStorage(dir_path= tmp_path)
        file_path = tmp_path / 'borrow_records.csv'
        assert not file_path.exists()
        with pytest.raises(FileNotFoundError, match='There is not a csv file at this path'):
            storage.import_from_csv()

class TestJsonFiles:
    
    def test_export_to_json(self, tmp_path: Path, library: Library):
        storage = DataStorage(dir_path= tmp_path)
        result = storage.export_to_json(data= library.inventory)
        file_path = tmp_path / 'books_inventory.json'
        assert file_path.is_file()
        assert result is True
        assert 'the hobbit' in file_path.read_text(encoding='utf-8')

    def test_export_to_json_when_data_not_a_list(self, tmp_path, library):
        storage = DataStorage(dir_path= tmp_path)
        with pytest.raises(TypeError, match='data should be a list'):
            storage.export_to_json(data='not a list')

    def test_export_to_json_when_data_is_not_a_list_of_books(self, tmp_path, library: Library):
        storage = DataStorage(dir_path= tmp_path)
        with pytest.raises(TypeError, match='must be Book objects'):
            storage.export_to_json(data=[1,2,3])

    def test_export_to_json_when_data_is_empty_list(self, tmp_path, library: Library):
        storage = DataStorage(dir_path= tmp_path)
        with pytest.raises(EmptyError, match='Can not export an empty book list'):
            storage.export_to_json(data=[])

    def test_import_from_json(self, tmp_path: Path, multiple_books: list[Book]):
        storage = DataStorage(dir_path=tmp_path)

        storage.export_to_json(data=multiple_books)

        data_from_json = storage.import_from_json()
        file_path = tmp_path / "books_inventory.json"

        assert file_path.is_file()
        assert isinstance(data_from_json, list)
        assert all(isinstance(book, Book) for book in data_from_json)
        assert len(data_from_json) == 3
        assert data_from_json[0].title == "the hobbit"


    def test_import_from_json_when_file_does_not_exist(self, tmp_path: Path):
        storage = DataStorage(dir_path=tmp_path)

        file_path = tmp_path / "books_inventory.json"

        assert not file_path.exists()

        with pytest.raises(FileNotFoundError, match="There is not a json file at this path"):
            storage.import_from_json()


    def test_import_from_json_with_invalid_json_structure(self, tmp_path: Path):
        storage = DataStorage(dir_path=tmp_path)

        file_path = tmp_path / "books_inventory.json"
        file_path.write_text('{"title": "not a list"}', encoding="utf-8")

        with pytest.raises(TypeError, match="JSON data must be a list of books"):
            storage.import_from_json()


    def test_import_from_json_with_invalid_book_data(self, tmp_path: Path):
        storage = DataStorage(dir_path=tmp_path)

        file_path = tmp_path / "books_inventory.json"
        file_path.write_text(
            '[{"title": "ab", "author": "George Orwell", "status": "available"}]',
            encoding="utf-8",
        )

        with pytest.raises(ValidationError):
            storage.import_from_json()


