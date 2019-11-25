import logging

from django import forms
from rest_framework import serializers

from social.models import Comment, Like, Post
from users.models import UserProfile

logger = logging.getLogger(__name__)


class PostSerializer(serializers.ModelSerializer):
    """ If we want to have username in response instead of id,
    we have to override author field using SerializerMethodField
    """
    author = serializers.SerializerMethodField('get_author_username')
    likes = serializers.SerializerMethodField('get_likes')
    comments = serializers.SerializerMethodField('get_comments')

    class Meta:
        model = Post
        # fields = ['content']
        fields = ['id', 'author', 'content', 'date_posted',
                  'location', 'image', 'likes', 'comments']

    def get_author_username(self, post):
        username = post.author.user.username
        return username

    def get_likes(self, post):
        likes = []
        for like in Like.objects.filter(post=post):
            serializer = LikeSerializer(like)
            likes.append(serializer.data)
        return likes

    def get_comments(self, post):
        comments = []
        for comment in post.comments.values():
            comment = Comment.objects.get(pk=comment['id'])
            serializer = CommentSerializer(comment)
            comments.append(serializer.data)
        return comments


class LikeSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_author_username')

    class Meta:
        model = Like
        fields = ['id', 'author', 'post', 'date_received']

    def get_author_username(self, like):
        username = like.author.user.username
        return username


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_author_username')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'text', 'date_created']

    def get_author_username(self, comment):
        username = comment.author.user.username
        return username
