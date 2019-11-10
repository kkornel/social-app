from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from . import admin as users_admin
from .views import register

urlpatterns = [
    # path('register/', register, name='register'),
    # path('login/',
    #      auth_views.LoginView.as_view(
    #          template_name='users/login.html',
    #          authentication_form=users_admin.CustomAuthForm),
    #      name='login'),
]
