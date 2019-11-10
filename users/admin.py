import logging

import requests as req
from django import forms
from django.contrib import admin
from django.contrib.auth import (authenticate, get_user_model,
                                 password_validation)
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       ReadOnlyPasswordHashField)
from django.contrib.auth.models import Group
from django.forms.widgets import EmailInput, PasswordInput, TextInput
from django.utils.safestring import mark_safe

from .models import MyUser

UserModel = get_user_model()

"""
#######################################################
Note:
On the official Django documentation site, they defined
those forms here in admin.py, instead of forms.py.
#######################################################
"""

logger = logging.getLogger(__name__)


class CustomAuthForm(AuthenticationForm):
    """
    I don't want to have labels on standrad LoginView such as "Email" or "Password",
    so I've created new CustomForm and changed those for empty strings.
    clean() method overrided, beacuse I didn't like the standard error output.
    The error was above the fields, I've changed it to be under instead.
    """
    username = forms.CharField(label='', widget=EmailInput(
        attrs={'class': 'validate', 'placeholder': 'Email'}))
    password = forms.CharField(label='', widget=PasswordInput(
        attrs={'placeholder': 'Password'}))

    error_messages = {
        'invalid_login': 'Incorrect email or  password.',
        'inactive': "This account is inactive.",
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password)
            if self.user_cache is None:
                # Original method:
                # raise self.get_invalid_login_error()

                # My custom method
                self.add_error(
                    'username', self.error_messages['invalid_login'])
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """

    email = forms.EmailField(label='', widget=forms.EmailInput(
        attrs={'placeholder': 'Email address'}),
        error_messages={'unique': mark_safe("Email already in use.  <a href=\"/login/\">Forgot Password?</a>")})

    username = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Username'}),
        error_messages={'unique': 'Account with this username already exists.'})

    password1 = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}))
        # error_messages={'invalid': mark_safe("Email already in use.  <a href=\"/password_reset/\">Forgot Password?</a>")})

    password2 = forms.CharField(
        label='', widget=forms.PasswordInput(
            attrs={'placeholder': 'Password confirmation'}))


    class Meta:
        model = MyUser
        fields = ('email', 'username')


    def clean_password2(self):
        logger.debug('Clean password running...')
        logger.debug('### Uncomment later!')

        # TODO: uncomment later. In order to validate passwords!
        # Check that the two password entries match
        # password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        # try:
        #     password_validation.validate_password(password2, self.instance)
        # except forms.ValidationError as error:
        #     # ! The one below should stay commented, because it is default one from Django. 
        #     # self.add_error('password1', error)
        #     self.add_error(
        #         'password1',  'Password must contain at least 8 characters.')
        # if password1 and password2 and password1 != password2:
        #     raise forms.ValidationError("Passwords do not match.")

        return password2

    def save(self, commit=True):
        logger.debug(
            "Save form (should never run, because I'm saving using user.save())")

        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'username', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'username', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
