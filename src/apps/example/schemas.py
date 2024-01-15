from datetime import datetime

from pydantic import BaseModel


class PersonIn(BaseModel):
    first_name: str
    last_name: str


class PersonOut(BaseModel):
    first_name: str = None
    last_name: str = None
    created_at: datetime = None

    class Config:
        orm_mode = True
