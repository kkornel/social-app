from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.views import PasswordResetConfirmView


class CaptchaPasswordResetForm(PasswordResetForm):
    """
    Custom PasswordResetForm only for styling EmailField.
    """
    email = forms.EmailField(label='', max_length=254, widget=forms.EmailInput(
        attrs={'placeholder': 'Email address'}))


class CustomSetPasswordForm(SetPasswordForm):
    """
    Custom SetPasswordForm  only for styling Password fields.
    A form that lets a user change set their password without entering the old
    password
    """
    new_password1 = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder': 'New password'}))
    # error_messages={'invalid': mark_safe("Email already in use.  <a href=\"/password_reset/\">Forgot Password?</a>")})

    new_password2 = forms.CharField(
        label='', widget=forms.PasswordInput(
            attrs={'placeholder': 'New password confirmation'}))
