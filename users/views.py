import logging

from django.contrib import messages
from django.shortcuts import redirect, render

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
            # TODO: Uncomment in order to save new users.
            # form.save()
            email = form.cleaned_data.get('email')
            messages.success(
                request, f'Account for {email} has been created! You are now able to log in.')
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

            # * Different parameters:
            # form.save(from_email='blabla@blabla.com',
            #           email_template_name='',
            #           html_email_template_name='users/password_reset_email.html',
            #           request=request,
            #           domain_override="aaaa",
            #           use_https=True,
            #           subject_template_name='users/password_reset_subject.txt')

            form.save(request=request,
                      html_email_template_name='users/password_reset_email.html',
                      subject_template_name='users/password_reset_email_subject.txt')

            # ? I think it is not nessccary.
            # user = form.save()
            # update_session_auth_hash(request, user)

            return redirect('password_reset_done')
        else:
            logger.debug('Form not valid')
    else:
        form = CaptchaPasswordResetForm()
    return render(request, 'users/password_reset.html', {'form': form})
