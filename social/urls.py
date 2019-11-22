from django.urls import path

from .views import (CommentCreateViewModal, CommentDeleteViewModal,
                    PostCreateView, PostDeleteView, PostDeleteViewModal,
                    PostDetail, PostListView, PostUpdateView, UserProfileView,
                    home, like_post)

urlpatterns = [
    # path('', home, name='home'),
    path('', PostListView.as_view(), name='home'),
    path('user/<str:username>/', UserProfileView.as_view(), name='user-profile'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    # AJAX
    path('like/', like_post, name='like-post'),

    # Modals
    path('post/comment/<int:pk>/delete/',
         CommentDeleteViewModal.as_view(), 
         name='delete-comment'),
    path('post/<int:pk>/del/',
         PostDeleteViewModal.as_view(), 
         name='delete-post'),
    path('post/<int:pk>/comment/', 
         CommentCreateViewModal.as_view(), 
         name='create-comment'),
]
