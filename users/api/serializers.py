import logging

from django import forms
from django.conf import settings
from django.contrib.auth import password_validation
from rest_framework import serializers

from social.api.serializers import (CommentSerializer, LikeSerializer,
                                    PostSerializer)
from users.models import MyUser, UserProfile

logger = logging.getLogger(__name__)


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = MyUser
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = MyUser(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )

        password1 = self.validated_data['password']
        password2 = self.validated_data['password2']

        try:
            password_validation.validate_password(password2, self.instance)
        except forms.ValidationError as error:
            raise serializers.ValidationError(
                {'password': 'Password must contain at least 8 characters.'})

        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError(
                {'password': 'Password must much'})

        user.set_password(password1)
        user.save()

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    # TODO followers, following
    posts = serializers.SerializerMethodField('get_user_posts')
    comments = serializers.SerializerMethodField('get_user_comments')
    likes = serializers.SerializerMethodField('get_user_likes')

    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'city', 'website',
                  'image', 'posts', 'comments', 'likes']

    def get_fields(self, *args, **kwargs):
        # Excluding user field, because we cannot update it.
        # Only bio, city, website changes are allowed.
        fields = super(UserProfileSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PATCH":
            fields['user'].required = False
        return fields

    def get_user_posts(self, userprofile):
        posts = []
        for post in userprofile.posts.order_by('-date_posted'):
            serializer = PostSerializer(post)
            posts.append(serializer.data)
        return posts

    def get_user_comments(self, userprofile):
        comments = []
        for comment in userprofile.comments.order_by('-date_created'):
            serializer = CommentSerializer(comment)
            comments.append(serializer.data)
        return comments

    def get_user_likes(self, userprofile):
        likes = []
        for like in userprofile.likes.all():
            serializer = LikeSerializer(like)
            likes.append(serializer.data)
        return likes
