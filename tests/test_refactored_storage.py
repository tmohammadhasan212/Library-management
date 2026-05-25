import pytest
from models.library import Library
from models.borrow_record import BorrowRecord
from library_system.refactored_data_storage import DataStorage
from pathlib import Path
from library_system.exceptions import EmptyError

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


