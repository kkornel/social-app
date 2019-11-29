from django.urls import path

from .views import (CommentCreateViewModal, CommentDeleteViewModal,
                    PostCreateView, PostCreateViewModal, PostDeleteView,
                    PostDeleteViewModal, PostDetail, PostListView,
                    PostUpdateView, PostUpdateViewModal, home, like_post)

urlpatterns = [
    # path('', home, name='home'),
    path('', PostListView.as_view(), name='home'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),

    path('post/<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    # AJAX
    path('like/', like_post, name='like-post'),

    # Modals
    path('post/new-modal/',
         PostCreateViewModal.as_view(),
         name='post-create-modal'),
    path('post/<int:pk>/update-modal/',
         PostUpdateViewModal.as_view(),
         name='post-update-modal'),
    path('post/<int:pk>/delete-modal/',
         PostDeleteViewModal.as_view(),
         name='post-delete-modal'),
    path('post/<int:pk>/create-comment/',
         CommentCreateViewModal.as_view(),
         name='comment-create-modal'),
    path('post/comment/<int:pk>/delete/',
         CommentDeleteViewModal.as_view(),
         name='comment-delete-modal'),
]
