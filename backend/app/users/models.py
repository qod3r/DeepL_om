from sqlalchemy import Column, Integer, String

from app.database import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    lastname = Column(String, nullable=False)
    name = Column(String, nullable=False)
    patronymic = Column(String, nullable=True)
    post = Column(String, nullable=False)
    password = Column(String, nullable=False)