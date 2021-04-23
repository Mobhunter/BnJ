from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class Chat(models.Model):
    users = models.ManyToManyField(User, db_table="m2m_user_chat", related_name="chats")
    def __str__(self) -> str:
        return f'{", ".join(map(lambda x: x.username, self.users.all()))} chat'


class Message(models.Model):
    text = models.TextField(default=str)
    created = models.DateTimeField(default=datetime.datetime.now)
    is_checked = models.BooleanField(default=False)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="+")
    def __str__(self) -> str:
        return f'{self.user.username}, {self.text[:21]}'
