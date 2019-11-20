from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.views import PasswordResetConfirmView

from .models import UserProfile


class CaptchaPasswordResetForm(PasswordResetForm):
    """
    Custom PasswordResetForm only for styling EmailField.
    """
    email = forms.EmailField(label='', max_length=254, widget=forms.EmailInput(
        attrs={'placeholder': 'Email address'}))


class CustomSetPasswordForm(SetPasswordForm):
    """
    Custom SetPasswordForm only for styling Password fields.
    A form that lets user set password without entering the old one.
    """
    new_password1 = forms.CharField(
        label='', widget=forms.PasswordInput(
            attrs={'placeholder': 'New password'}))

    new_password2 = forms.CharField(
        label='', widget=forms.PasswordInput(
            attrs={'placeholder': 'New password confirmation'}))


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']
