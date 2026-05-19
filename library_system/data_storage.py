from pathlib import Path
import csv
from .library import Library
import json
from .book import Book
from typing import TypedDict
from library_system.library import BorrowRecord

class RecordToCSV(TypedDict):
    name : str
    book_id : int
    borrow_time : float
    return_time : float | str

class DataStorage:
    def __init__(self, dir_path:Path | None = None):
        self.dir_path = dir_path

    @property
    def dir_path(self) -> Path:
        return self.__dir_path
    
    @dir_path.setter
    def dir_path(self, path:Path):
        if path is None:
            self.__dir_path: Path = Path(__file__).parent.parent / 'data'
        else:
            self.__dir_path = Path(path)
        self.__dir_path.mkdir(parents=True, exist_ok=True)

    @property
    def create_library_storage(self) -> Path:
        try:
            library_storage_path = self.dir_path / 'library.csv'
            library_storage_path.touch(exist_ok=True)
            return library_storage_path
        except Exception as e:
            raise RuntimeError(f"Failed to create library storage: {e}") from e
        
    @property
    def create_borrows_storage(self) -> Path:
        try:
            borrows_storage_path = self.dir_path / 'borrows.csv'
            borrows_storage_path.touch(exist_ok=True)
            return borrows_storage_path
        except Exception as e:
            raise RuntimeError(f"Failed to create library storage: {e}") from e
        
    def _write_to_csv(self, file_path : Path, headers : list[str], data: list[RecordToCSV]):
        try:

            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                dict_writer = csv.DictWriter(file, fieldnames=headers)
                dict_writer.writeheader()
                dict_writer.writerows(data)
            print(f'Data has been successfully exported to {file_path}')
        except Exception as e:
            raise RuntimeError(f'something went wrong with the writing of csv file. {e}')

            
    def export_to_csv(self, data:list[BorrowRecord], file_path : Path):
        
        file_path = Path(file_path)
        headers = ['name', 'book_id', 'borrow_time', 'return_time']
        final_data : list[RecordToCSV] = []
        if not data:
            raise ValueError('Do not provide an empty list for data.')
        
        if file_path.suffix != '.csv':
            raise ValueError(f'The file is not a csv file at this path : {file_path}')
        
        for record in data:
            if not isinstance(record['book'], Book):
                raise ValueError('the type of the book in the borrow records is not a Book object.')

            final_data.append({
                'name':record['name'], 'book_id':record['book'].id, 'borrow_time':record['borrow_time'], 'return_time': record['return_time'] if record['return_time'] is not None else ''})
            
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise RuntimeError(f'Failed to create directory {file_path.parent}: {e}')
        
        self._write_to_csv(file_path, headers, final_data)
        
        
        
    def _read_csv_file(self, file_path : Path):
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                expected_headers = ['name', 'book_id', 'borrow_time', 'return_time']
                if not all(header in reader.fieldnames for header in expected_headers):
                    raise ValueError(f'there is a mismatch between expected headers and csv headers\n{expected_headers} != {reader.fieldnames}')
                data = list(reader)
                return data
            
        except Exception as e:
            raise RuntimeError(f'something went wrong with the reading of csv file. {e}')
        
    def _convert_record(self, record: dict) -> dict:
        converted_record = {'name':record['name'],'book_id':int(record['book_id']),'borrow_time': float(record['borrow_time']),'return_time': float(record['return_time']) if record['return_time'] and record['return_time'] != '' else None}

        return converted_record

    
    def import_from_csv(self, file_path : Path) -> list:
        file_path = Path(file_path)
        final_data = []
        if not file_path.is_file():
            raise ValueError(f'There is no file at : {file_path}')
        if file_path.suffix != '.csv':
            raise ValueError(f'The file is not a csv file at this path : {file_path}')
        
        data = self._read_csv_file(file_path)
        
        if not data:
            print("Warning: CSV file has headers but no data")
            return []  # or handle appropriately
        
        final_data = [self._convert_record(record) for record in data]
        
        print(f'Data has successfully imported from this path: {file_path}')
        return final_data
    

        
    def export_to_json(self, file_path : Path, data : list):
        file_path = Path(file_path)
        final_data = []
        if not data:
            raise ValueError('Do not provide an empty list for data.')
        
        if file_path.suffix.lower() != '.json':
            raise ValueError(f'The file is not a json file at this path : {file_path}')
        
        for one_book in sorted(data, key= lambda book: book.id):
            final_data.append({
                'id':one_book.id,
                'title':one_book.title,
                'author':one_book.author,
                'status':one_book.status 
            })

        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)

        except Exception as e:
            raise RuntimeError(f'Failed to create directory {file_path.parent}: {e}')
        
        try:
            with open(file_path, mode='w', encoding='utf-8') as file:
                json.dump(final_data, file, indent=2)

            print(f'Data has been successfully exported to: {file_path}')

        except Exception as e:
            raise RuntimeError(f'something went wrong with writing data into json file.\n{e}')
        
    
    def import_from_json(self, file_path : Path) -> list:
        file_path = Path(file_path)
        if not file_path.is_file():
            raise ValueError(f'There is no file at : {file_path}')
        if file_path.suffix != '.json':
            raise ValueError(f'The file is not a json file at this path : {file_path}')
        
        with open(file_path, encoding='utf-8') as file:
            data = json.load(file)

        return Library.convert_to_book_obj(data)
    
    
    


        

        

    







    
    
    

    

        


        