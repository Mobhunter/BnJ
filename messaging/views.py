from django.shortcuts import render
from django.http import HttpRequest
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required()
def message_board_view(request: HttpRequest):
    return render(request, "messaging/message_board.html")

@login_required()
def chat_view(request: HttpRequest):
    return render(request, "messaging/chat.html")