from pathlib import Path
import csv
from models.library import Library
import json
from models.book import Book
from models.borrow_record import BorrowRecord

class DataStorage:
    def __init__(self, dir_path:Path | None = None):
        self.__dir_path = self._prepare_dir_path(dir_path)

    @property
    def dir_path(self) -> Path:
        return self.__dir_path
    
    @dir_path.setter
    def dir_path(self, path:Path | None):
        self.__dir_path = self._prepare_dir_path(path)


        
    @staticmethod
    def _prepare_dir_path(dir_path : Path | None) -> Path:
        resolved_path = (
            Path(__file__).parent.parent / 'data'
            if dir_path is None
            else Path(dir_path).resolve()
        )
        resolved_path.mkdir(parents= True, exist_ok= True)
        return resolved_path