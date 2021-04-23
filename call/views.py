from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.urls import reverse


def call_view(request):
    return render(request, "call/main.html")