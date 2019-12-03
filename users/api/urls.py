from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (ApiUserProfileView, GetAllUsersApiView, TestView,
                    UserProfilesCreateView, UserProfilesPostListCreateView,
                    UserProfilesView, UserProfileView, registration_view)

app_name = 'users'

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='profile'),


    path('profiles/', UserProfilesView.as_view(), name='profiles'),

    # path('test/', TestView.as_view(), name='test'),
    path('create/', UserProfilesCreateView.as_view(), name='create'),
    path('list-create/', UserProfilesPostListCreateView.as_view(), name='list-create'),
    path('getprofile/<token>/', ApiUserProfileView.as_view(), name='getprofile'),

    # Development
    path('users/', GetAllUsersApiView.as_view(), name='get-all-users'),

]


urlpatterns = format_suffix_patterns(urlpatterns)
