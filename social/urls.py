from django.urls import path

from .views import PostCreateView, PostListView, home

urlpatterns = [
    # path('', home, name='home'),
    path('', PostListView.as_view(), name='home'),
    path('post/create/', PostCreateView.as_view(), name='post-create'),
]
