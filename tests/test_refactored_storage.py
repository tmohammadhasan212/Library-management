import pytest
from models.library import Library
from library_system.refactored_data_storage import DataStorage
from pathlib import Path

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


