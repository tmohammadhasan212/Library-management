from pathlib import Path
import csv
from models.library import Library
import json
from models.book import Book
from models.borrow_record import BorrowRecord
from uuid import UUID
from library_system.exceptions import EmptyError

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
        
        if not data:
            raise EmptyError("Can not export an empty borrow records list.")
        
        if not all(isinstance(record, BorrowRecord) for record in data):
            raise TypeError("all items in list must be BorrowRecord objects")
        
        dict_records = [record.model_dump(mode='json') for record in data]
        
        self._write_to_csv(file_path, dict_records)
        return True
    
    def _read_csv_file(self, file_path: Path) -> list[dict]:
        try:
            headers = ['uid','book_uid','borrower_name', 'title', 'status', 'borrow_time', 'return_time']
            with open(file_path, encoding='utf-8') as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames
                if fieldnames is None:
                    raise ValueError("CSV file has no headers.")
                if not all(header in fieldnames for header in headers):
                    raise ValueError(
                        f'There was a mismatch between csv headers and expected headers.\nExpected: {headers}, got: {reader.fieldnames}')
                return list(reader)
        except Exception as e:
            raise RuntimeError(f'something went wrong during reading process. {e}') from e
        
    def _convert_record(self, record: dict) -> dict:
        return {
            **record,
            "return_time": None if record["return_time"] == "" else record["return_time"],
        }
        
    def import_from_csv(self) -> list[BorrowRecord]:
        file_path = self.dir_path / 'borrow_records.csv'
        result: list[BorrowRecord] = []
        if not file_path.is_file():
            raise FileNotFoundError(f"There is not a csv file at this path: {file_path}")
        data = self._read_csv_file(file_path)
        for record in data:
            result.append(BorrowRecord(**self._convert_record(record)))
        return result
    
    def export_to_json(self, data: list[Book]) -> bool:
        if not isinstance(data, list):
            raise TypeError(f"data should be a list. Got a {type(data).__name__}")
        
        if not data:
            raise EmptyError("Can not export an empty book list.")
        
        if not all(isinstance(book, Book) for book in data):
            raise TypeError("all items in list must be Book objects")
        
        file_path = self.dir_path / 'books_inventory.json'
        final_data : list[dict] = [book.model_dump(mode='json') for book in data]

        try:
            with open(file_path, mode='w', encoding='utf-8') as f:
                json.dump(final_data, f, indent=2)
                return True
        except Exception as e:
            raise RuntimeError(f'Something went wrong with json writing. {e}') from e
        
    def import_from_json(self) -> list[Book]:
        file_path = self.dir_path / 'books_inventory.json'

        if not file_path.is_file():
            raise FileNotFoundError(f"There is not a json file at this path: {file_path}")
        
        try:
            with open(file_path, encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            raise RuntimeError(f"Something went wrong with the json reading process. {e}") from e
        
        if not isinstance(data, list):
            raise TypeError("JSON data must be a list of books.")

        final_data : list[Book] = [Book(**book) for book in data]
        return final_data
