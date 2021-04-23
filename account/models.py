from django.db import models
import django.contrib.postgres.fields as ps_models
import uuid
from django.contrib.auth.models import User
import datetime


def post_upload(instance, filename):
    d = datetime.datetime.now()
    path = f"audio/{d.year}/{d.month}/{d.day}/{uuid.uuid4()}{'.' + filename.split('.')[-1] if len(filename.split('.')) > 1 else ''}"
    return path


def img_icon_upload(instance, filename):
    path = f"images/{instance.user.id}/icon{'.' + filename.split('.')[-1] if len(filename.split('.')) > 1 else ''}"
    return path


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "genre"


class Instrument(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "instrument"


class UserInfo(models.Model):
    age = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userinfo")
    genres = models.ManyToManyField(Genre, db_table="m2m_userinfo_genre", related_name="userinfo")
    instruments = models.ManyToManyField(Instrument, db_table="m2m_userinfo_instruments", related_name="userinfo")
    favourite_bands = ps_models.ArrayField(models.CharField(max_length=255), default=list)
    songs = ps_models.ArrayField(models.CharField(max_length=255), default=list)
    img = models.ImageField(null=True, upload_to=img_icon_upload, default="base/no.jpg")

    def __str__(self):
        return f"{self.user.username}`s userinfo"

    class Meta:
        db_table = "userinfo"


class UserStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userstatus")
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}`s userstatus"


class Post(models.Model):
    created = models.DateTimeField(default=datetime.datetime.now)
    message = models.TextField(null=True)
    audio = models.FileField(upload_to=post_upload, null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return f"{self.user.username}`s post, created at {self.created}"

    class Meta:
        db_table = "post"