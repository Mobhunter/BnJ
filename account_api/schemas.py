from pydantic import BaseModel
from typing import List, Optional
import datetime


class PostModel(BaseModel):
    date: datetime.date
    message: Optional[str] = None
    audio: Optional[str] = None


class AccountInfoModel(BaseModel):
    name: str
    age: int
    img: str
    genre: List[str]
    instruments: List[str]
    posts: List[PostModel]
    songs: List[str]
    favourite_bands: List[str]
    is_owner: bool
    link: str


class PostInputModel(BaseModel):
    audio: Optional[str]
    message: Optional[str]