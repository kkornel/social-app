import logging

from django import forms
from django.contrib.auth import password_validation
from rest_framework import serializers

from users.models import MyUser, UserProfile

logger = logging.getLogger(__name__)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'city', 'website', 'image']


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type' : 'password'}, write_only=True)

    class Meta:
        model = MyUser
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password' : {'write_only' : True}
        }

    def save(self):
        user = MyUser(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        logger.debug(user)
        password1=self.validated_data['password']
        password2=self.validated_data['password2']

        try:
            password_validation.validate_password(password2, self.instance)
        except forms.ValidationError as error:
            raise serializers.ValidationError({'password' : 'Password must contain at least 8 characters.'})
        
        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError({'password' : 'Password must much'})

        user.set_password(password1)
        user.save()
        
        return user
