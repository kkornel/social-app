
from django import forms
from django.contrib.auth.forms import PasswordResetForm


class CaptchaPasswordResetForm(PasswordResetForm):
    """
    Custom PasswordResetForm only for styling EmailField.
    """
    email = forms.EmailField(label='', max_length=254, widget=forms.EmailInput(
        attrs={'placeholder': 'Email address'}))
