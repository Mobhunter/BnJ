from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.registration_view, name='register'),
    path('cabinet/', views.cabinet_view, name='cabinet'),
    path('logout/', views.logout_view, name='logout')
]