from pydantic import BaseModel, Field, PositiveInt, ConfigDict, model_validator
from typing import Annotated, Literal, ClassVar

class Book(BaseModel):
    model_config = ConfigDict(validate_assignment=True, str_to_lower=True, str_strip_whitespace=True)
    title : Annotated[str, Field(min_length=3)]
    uid : PositiveInt | None = None
    author : Annotated[str, Field(min_length=3)]
    status : Literal['available', 'borrowed'] = 'available'
    counter : ClassVar[int] = 0

    @model_validator(mode='after')
    def check_id(self) -> 'Book':
        if self.uid is None:
            type(self).counter +=1
            object.__setattr__(self, 'uid', type(self).counter)
        else:
            if self.uid > type(self).counter:
                type(self).counter = self.uid
        return self
    
    @classmethod
    def reset_counter(cls) -> None:
        cls.counter = 0
    