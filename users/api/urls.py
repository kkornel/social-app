from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import (ApiUserProfileView, TestView, UserProfileCreateView,
                    UserProfilePostListCreateView, UserProfileView,
                    registration_view)

app_name = 'users'

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('test/', TestView.as_view(), name='test'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('create/', UserProfileCreateView.as_view(), name='create'),
    path('list-create/', UserProfilePostListCreateView.as_view(), name='list-create'),
    path('getprofile/<token>/', ApiUserProfileView.as_view(), name='getprofile'),
]
