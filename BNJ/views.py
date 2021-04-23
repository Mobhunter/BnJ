from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse


def index_view(request: HttpRequest):
    return redirect(reverse("account:cabinet"))