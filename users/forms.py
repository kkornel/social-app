from bootstrap_modal_forms.forms import BSModalForm
from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

from .models import MyUser, UserProfile


class CaptchaPasswordResetForm(PasswordResetForm):
    """Custom PasswordResetForm only for styling EmailField."""
    email = forms.EmailField(label='',
                             max_length=254,
                             widget=forms.EmailInput(
                                 attrs={'placeholder': 'Email address'}))


class CustomSetPasswordForm(SetPasswordForm):
    """
    Custom SetPasswordForm only for styling Password fields.
    A form that lets user set password without entering the old one.
    """
    new_password1 = forms.CharField(label='',
                                    widget=forms.PasswordInput(
                                        attrs={'placeholder': 'New password'}))

    new_password2 = forms.CharField(label='',
                                    widget=forms.PasswordInput(
                                        attrs={'placeholder': 'New password confirmation'}))


class MyUserUpdateFormModal(BSModalForm):

    class Meta:
        model = MyUser
        fields = ['email']


class UserProfileUpdateFormModal(BSModalForm):
    bio = forms.CharField(required=False,
                          max_length=300,
                          widget=forms.Textarea(attrs={
                              'rows': 6,
                              'cols': 10,
                              #   'style': 'resize:none;',
                              'style': 'resize:none; background-color: #15181c; color: #d9d9d9;',
                              'placeholder': 'Tell others a little bit about yourself!',
                          }))
    city = forms.CharField(required=False,
                           max_length=100,
                           widget=forms.TextInput(attrs={
                               'placeholder': 'Oslo, Norway',
                           }))

    website = forms.CharField(required=False,
                              max_length=30,
                              widget=forms.TextInput(attrs={
                                  'placeholder': 'stackoverflow.com',
                              }))

    image = forms.ImageField(label='Photo',
                             required=False,
                             widget=forms.FileInput)

    delete_current_image = forms.BooleanField(label='Delete current image checkbox:',
                                              required=False)

    class Meta:
        model = UserProfile
        fields = ['bio', 'city', 'website', 'image']


# Below are not used Forms.
# They are standard Django Forms,
# but I replaced them with Modals.

class MyUserUpdateForm(forms.ModelForm):
    """Not using Modals. Standard Django template"""
    class Meta:
        model = MyUser
        fields = ['email']


class UserProfileUpdateForm(forms.ModelForm):
    """Not using Modals. Standard Django template"""
    bio = forms.CharField(required=False,
                          max_length=300,
                          widget=forms.Textarea(attrs={
                              'rows': 6,
                              'cols': 10,
                              #   'style': 'resize:none;',
                              'style': 'resize:none; background-color: #15181c; color: #d9d9d9;',
                              'placeholder': 'Tell others a little bit about yourself!',
                          }))
    city = forms.CharField(required=False,
                           max_length=100,
                           widget=forms.TextInput(attrs={
                               'placeholder': 'Oslo, Norway',
                           }))

    website = forms.CharField(required=False,
                              max_length=30,
                              widget=forms.TextInput(attrs={
                                  'placeholder': 'Do you have any domain?',
                              }))

    image = forms.ImageField(label='Photo',
                             required=False,
                             widget=forms.FileInput)

    delete_current_image = forms.BooleanField(label='Delete current image checkbox:',
                                              required=False)

    class Meta:
        model = UserProfile
        fields = ['bio', 'city', 'website', 'image']
