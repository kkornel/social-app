import logging

import requests
from django.contrib import messages
from django.shortcuts import redirect, render

from social_app import settings

from .admin import UserCreationForm
from .decorators import check_recaptcha
from .forms import CaptchaPasswordResetForm

logger = logging.getLogger(__name__)


@check_recaptcha
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        logger.debug(f"email: {request.POST['email']}")
        logger.debug(f"username: {request.POST['username']}")
        logger.debug(f"password1: {request.POST['password1']}")
        logger.debug(f"password2: {request.POST['password2']}")
        if form.is_valid() and request.recaptcha_is_valid:
            logger.debug('Form valid')
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your account has been created! You are now able to log in.')
            return redirect('login')
        else:
            logger.debug('Form not valid')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


@check_recaptcha
def reset_password(request):
    if request.method == 'POST':
        form = CaptchaPasswordResetForm(request.POST)
        if form.is_valid() and request.recaptcha_is_valid:
            logger.debug('Form valid')
            form.save(from_email='blabla@blabla.com',
                      html_email_template_name='users/password_reset_email.html', request=request, domain_override="aaaa", use_https=True, subject_template_name='users/password_reset_subject.txt')
            messages.success(request, 'New comment added with success!')
            # user = form.save()
            # update_session_auth_hash(request, user)
            # messages.success(request, _(
            # 'Your password was successfully updated!'))
            return redirect('password_reset_done')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        form = CaptchaPasswordResetForm()
    return render(request, 'users/password_reset.html', {
        'form': form
    })
