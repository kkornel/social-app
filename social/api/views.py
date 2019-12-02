import logging

from rest_framework import filters, generics, mixins, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from social.models import Comment, Like, Post
from users.decorators import func_log

from .serializers import CommentSerializer, LikeSerializer, PostSerializer

logger = logging.getLogger(__name__)


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (AllowAny, )


class PostViewApi(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date_posted']
    ordering = ['-date_posted']

    permission_classes = (AllowAny, )

    # @func_log
    # def get(self, request, *args, **kwargs):
    #     return self.list(self, request, *args, **kwargs)


class LikeViewApi(APIView):
    # serializer_class = LikeSerializer
    # queryset = Like.objects.all()

    permission_classes = (AllowAny, )

    @func_log
    def get(self, request, *args, **kwargs):
        print(request)
        print(request.data)

        qs = Like.objects.all()
        serializer = LikeSerializer(qs, many=True)
        return Response(serializer.data)


class CommentViewApi(APIView):
    # serializer_class = CommentSerializer
    # queryset = Comment.objects.all()

    permission_classes = (AllowAny, )

    @func_log
    def get(self, request, *args, **kwargs):
        print(request)
        print(request.data)

        qs = Comment.objects.all()
        serializer = CommentSerializer(qs, many=True)
        return Response(serializer.data)

    # @func_log
    # def get(self, request, *args, **kwargs):
    #     print(request)
    #     print(request.data)

    #     qs = Post.objects.all()
    #     serializer = PostSerializer(qs, many=True)
    #     return Response(serializer.data)
