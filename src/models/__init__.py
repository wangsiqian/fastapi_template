from datetime import datetime

from passlib.hash import bcrypt
from sqlmodel import Field, SQLModel


class Person(SQLModel, table=True):
    __tablename__ = 'person'

    first_name: str = Field(max_length=256, primary_key=True)
    last_name: str = Field(max_length=256)

    created_at: datetime = Field(default_factory=datetime.utcnow)


class User(SQLModel, table=True):
    __tablename__ = 'user'

    id: int | None = Field(primary_key=True)
    username: str = Field(max_length=32)
    password: str = Field(max_length=64)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    async def new(cls, username: str, password: str):
        hashed_password = bcrypt.hash(password)
        user = User(username=username, password=hashed_password)
        return user

    async def verify_password(self, password: str):
        """使用 bcrypt 加密算法验证密码
        """
        return bcrypt.verify(password, self.password)
