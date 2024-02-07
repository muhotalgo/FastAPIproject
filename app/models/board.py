from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class Member(Base):
    __tablename__ = 'board'

    bno = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(18), nullable=False)
    userid = Column(String(18), nullable=False)
    regdate = Column(DateTime, default=datetime.now)
    view = Column(Integer, default=0)
    contents = Column(Text, nullable=False)
