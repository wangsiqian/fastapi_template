from pydantic import BaseModel


class UserIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    username: str

    class Config:
        orm_mode = True


class LoginOut(BaseModel):
    token: str
    user: UserOut
