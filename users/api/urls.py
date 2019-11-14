from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import (ProfileCreateView, ProfilePostListCreateView, ProfileView,
                    TestView, registration_view)

app_name = 'users'

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('test/', TestView.as_view(), name='test'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('create/', ProfileCreateView.as_view(), name='create'),
    path('list-create/', ProfilePostListCreateView.as_view(), name='list-create')
]
