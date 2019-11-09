import logging

from django.shortcuts import render

from .admin import UserCreationForm

logger = logging.getLogger(__name__)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        logger.debug(f"email: {request.POST['email']}")
        logger.debug(f"username: {request.POST['username']}")
        logger.debug(f"password1: {request.POST['password1']}")
        logger.debug(f"password2: {request.POST['password2']}")
        if form.is_valid():
            logger.debug('Form valid')
        else:
            logger.debug('Form not valid')
    else:
        #     form = UseCreationForm(request.POST)
        #     if form.is_valid():
        #         print()
        # else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})
