from datetime import datetime

from pydantic import BaseModel


class PersonIn(BaseModel):
    first_name: str
    last_name: str


class PersonOut(BaseModel):
    first_name: str
    last_name: str
    created_at: datetime
