from pydantic import BaseModel, Field, PositiveInt, ConfigDict
from typing import Literal
from uuid import UUID, uuid4

class BorrowRecord(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        str_to_lower=True,
        str_strip_whitespace=True,
        str_min_length=3,
        str_max_length= 30
    )
    uid: UUID = Field(default_factory=uuid4)
    borrower_name: str
    title: str
    status: Literal['borrowed', 'returned'] = 'borrowed'
    borrow_time: float
    return_time: float | None = None


