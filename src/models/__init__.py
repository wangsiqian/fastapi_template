from datetime import datetime

from passlib.hash import bcrypt
from sqlalchemy import VARCHAR, BigInteger, Column, DateTime

from extensions.sqlalchemy import Base


class Person(Base):
    __tablename__ = 'person'

    first_name = Column(VARCHAR(255), primary_key=True)
    last_name = Column(VARCHAR(255))

    created_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    username = Column(VARCHAR(11))
    password = Column(VARCHAR(60))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    @classmethod
    async def new(cls, username: str, password: str):
        hashed_password = bcrypt.hash(password)
        user = User(username=username, password=hashed_password)
        return user

    async def verify_password(self, password: str):
        """使用 bcrypt 加密算法验证密码
        """
        return bcrypt.verify(password, self.password)
