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
    
    def _write_to_csv(self, file_path : Path, data: list[dict]):
        headers = data[0].keys()
        try:

            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                dict_writer = csv.DictWriter(file, fieldnames=headers)
                dict_writer.writeheader()
                dict_writer.writerows(data)
            print(f'Data has been successfully exported to {file_path}')
        except Exception as e:
            raise RuntimeError(f'something went wrong with the writing of csv file. {e}')

            
    def export_to_csv(self, data:list[BorrowRecord]) -> bool:

        file_path = self.__dir_path / 'borrow_records.csv'

        if not isinstance(data, list):
            raise TypeError(f"data should be a list. Got a {type(data).__name__}")
        
        if not all(isinstance(record, BorrowRecord) for record in data):
            raise TypeError("all items in list must be BorrowRecord objects")
        
        dict_records = [record.model_dump(mode='json') for record in data]
        
        self._write_to_csv(file_path, dict_records)
        return True