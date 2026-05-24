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
    