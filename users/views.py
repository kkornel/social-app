import logging

import requests
from django.contrib import messages
from django.shortcuts import render

from social_app import settings

from .admin import UserCreationForm
from .decorators import check_recaptcha

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
            # form.save()
            messages.success(request, 'New comment added with success!')
            # return redirect('comments')
        else:
            logger.debug('Form not valid')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})
