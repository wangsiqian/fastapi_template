from pydantic import BaseModel


class UserIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str


class LoginOut(BaseModel):
    token: str
    user: UserOut
