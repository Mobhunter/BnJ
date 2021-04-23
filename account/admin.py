from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Genre)
admin.site.register(models.Instrument)
admin.site.register(models.UserInfo)
admin.site.register(models.Post)
admin.site.register(models.UserStatus)