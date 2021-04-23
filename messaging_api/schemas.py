import datetime
from pydantic import BaseModel
from typing import Optional, List

class ChatModel(BaseModel):
    name: str
    icon: str
    last_message: str
    lm_date: str
    link: str
    date: datetime.datetime

class MessageModel(BaseModel):
    text: str
    date: datetime.datetime
    author: str
    is_checked: bool
    id: Optional[int] = None


class UserBaseModel(BaseModel):
    name: str
    icon: str
    link: str


class UserModel(UserBaseModel):
    chats: List[ChatModel]


class MessageAnswerModel(BaseModel):
    sender: UserBaseModel
    reciever: UserBaseModel
    chat_story: List[MessageModel]