from typing import Literal
class Book:
    __counter = 0
    def __init__(
            self, title : str, author : str, status : Literal['available', 'borrowed']= 'available', id : int | None = None):
        Book.__counter += 1
        if id is not None:
            self.id = int(id)
            # Update counter if needed
            if self.id >= Book.__counter:
                Book.__counter = self.id
        else:
            self.id = Book.__counter  
        self.title = title
        self.author = author
        self.status = status
    
    @classmethod
    def reset_counter(cls):
        """Reset counter - useful for testing"""
        cls.__counter = 0

    @staticmethod
    def __validate_string(value : str, field_name: str):
        if not isinstance(value, str):
            raise ValueError(f'Invalid {field_name}. it must be a string')
        if not value.strip():
            raise ValueError(f'{field_name} can not be empty.')

    @property
    def title(self) -> str:
        return self.__title
    
    @title.setter
    def title(self, value):
        self.__validate_string(value, 'title')
        self.__title = value

    @property
    def author(self):
        return self.__author
    
    @author.setter
    def author(self, value):
        self.__validate_string(value, 'author')
        self.__author = value

    @property
    def status(self):
        return self.__status
    
    @status.setter
    def status(self, value):
        valid_statuses = ['available', 'borrowed']
        self.__validate_string(value, 'status')
        if not value.lower() in valid_statuses:
            raise ValueError(f'Status must be one of: {valid_statuses}')
        self.__status = value.lower()
    
    def __str__(self):
        return f'{self.id} | {self.title} | {self.author} | {self.status}'
    
    def __eq__(self, other_book):
        if not isinstance(other_book, Book):
            raise ValueError('Other object must be a Book type.')
        
        return (self.id == other_book.id and self.title == other_book.title and self.author == other_book.author and self.status == other_book.status)
        
    

        
    
        
        
        