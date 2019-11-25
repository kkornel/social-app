from django.urls import path

from .views import CommentViewApi, LikeViewApi, PostRetrieveUpdateDestroyAPIView, PostViewApi

app_name = 'social'

urlpatterns = [
    path('posts/', PostViewApi.as_view(), name='posts'),
    path('comments/', CommentViewApi.as_view(), name='comments'),
    path('likes/', LikeViewApi.as_view(), name='likes'),
    path('post/<int:pk>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='post'),
]
