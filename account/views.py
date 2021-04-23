from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.urls import reverse
import jose.jwt as jwt
import uuid
from .models import UserInfo, Genre, Instrument, UserStatus

from .forms import LoginForm, RegistrationForm, PasswordChangeForm, PasswordResetForm

REMEMBER_ME_EXPIRY = 31536000 # A year


def login_view(request: HttpRequest):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'account/login.html', {"form": form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if not form.check():
            return render(request, 'account/login.html', {"form": form})
        if request.user.is_authenticated:
            logout(request)
        login(request, form.user)
        if form.cleaned_data["remember_me"]:
            request.session.set_expiry(REMEMBER_ME_EXPIRY)
        else:
            request.session.set_expiry(0)
        if request.GET.get("next"):
            return redirect(request.GET.get("next"))
        return redirect(reverse("account:cabinet"))


def registration_view(request: HttpRequest):
    if request.method == 'GET':
        form = RegistrationForm()
        return render(request, 'account/register.html', {"form": form})
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if not form.check():
            return render(request, 'account/register.html', {"form": form})
        
        new_user = None
        new_userinfo = None
        try:
            new_user = User(email=form.cleaned_data["email"], username=form.cleaned_data["username"], is_active=True) # Set is_active to false, if you are going to confi
            new_user.set_password(form.cleaned_data["password"])
            new_user.save()

            new_userinfo = UserInfo(age=form.cleaned_data["age"], user=new_user)
            new_userinfo.save()
            for genre in form.genres:
                new_userinfo.genres.add(Genre.objects.get(name=genre))
            for tool in form.instruments:
                new_userinfo.instruments.add(Instrument.objects.get(name=tool))
            new_userinfo.save()

            new_userstatus = UserStatus(user=new_user)
            new_userstatus.save()
        except Exception as ex:
            if new_user is not None:
                new_user.delete()
            if new_userinfo is not None:
                new_userinfo.delete()
            raise ex 
        return redirect(reverse("account:login"))


@login_required()
def logout_view(request: HttpRequest):
    if request.user.is_authenticated:
        logout(request, request.user)
    return HttpResponse("You're logged out")
    

@login_required()
def cabinet_view(request: HttpRequest):
    return render(request, "account/cabinet.html")