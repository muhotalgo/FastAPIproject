from datetime import datetime

from pydantic import BaseModel


class Member(BaseModel):
    bno: int
    title: str
    userid: str
    regdate: datetime
    view: int
    contents: str

    class Config:
        from_attributes = True



class NewBoard(BaseModel):
    title: str
    userid: str
    contents: str
