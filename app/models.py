from sqlalchemy import Column, Integer, String, DateTime, func
from .db import Base

# Account model
class Account(Base):
    __tablename__ = "accounts"

    _id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    last_login = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"User(id={self._id}, username='{self.username}')"


