from django.urls import path

from .views import (PostCreateView, PostDeleteView, PostDetail, PostListView,
                    PostUpdateView, UserProfileView, home, like_post)

urlpatterns = [
    # path('', home, name='home'),
    path('', PostListView.as_view(), name='home'),
    path('user/<str:username>/', UserProfileView.as_view(), name='user-profile'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    #
    path('like/', like_post, name='like-post'),
]
