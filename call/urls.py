from django.urls import path
from . import views

app_name = "call"
urlpatterns = [
    path("main/", views.call_view, name="main")
]