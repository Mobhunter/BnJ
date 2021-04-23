from django.urls import path
from . import views

app_name = "messaging"

urlpatterns = [
    path('message_board/', views.message_board_view, name='message_board'),
    path('chat/', views.chat_view, name="chat")
]