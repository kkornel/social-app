import logging

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .admin import UserCreationForm
from .decorators import check_recaptcha
from .forms import CaptchaPasswordResetForm
from .models import MyUser
from .tokens import account_activation_token

logger = logging.getLogger(__name__)


@check_recaptcha
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        logger.debug(f"email: {request.POST['email']}")
        logger.debug(f"username: {request.POST['username']}")
        logger.debug(f"password1: {request.POST['password1']}")
        logger.debug(f"password2: {request.POST['password2']}")
        # if form.is_valid() and request.recaptcha_is_valid:
        if form.is_valid():
            logger.debug('Form valid')
            # Password confirmation.
            user = form.save(commit=False)
            user.is_active = False
            # TODO: Uncomment in order to save new users.
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user),
            logger.debug(f'uid: {uid}')
            logger.debug(f'token: {token}')
            logger.debug(f'token: {token[0]}')
            logger.debug(f'user: {user}')
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                # 'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': token[0],
            })

            # 1 Way:
            to_email = form.cleaned_data.get('email')
            # email = EmailMessage(email_subject, message, to=[
            #                      to_email])
            # email.send()
            send_mail(
                email_subject,
                message,
                'from@example.com',
                [to_email],
                fail_silently=False,
                html_message=message
            )
            # 1 Way end
            # 2 Way:
            # email_subject = 'Activate Your Account second way'
            # user.email_user(email_subject, message)
            # 2 Way end
            email = form.cleaned_data.get('email')
            messages.success(
                request, f'Account for {email} has been created! You are now able to log in.')
            return redirect('login')
        else:
            logger.debug('Form not valid')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        logger.debug(f'uidb64: {uidb64}')
        uid = force_text(urlsafe_base64_decode(uidb64))
        logger.debug(f'uid: {uid}')
        logger.debug(f'token: {token}')
        user = MyUser.objects.get(pk=uid)
        logger.debug(f'token: {token}')
        logger.debug(f'user: {user}')

    except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None

    logger.debug(f'user: {user}')
    logger.debug(
        f'account_activation_token: {account_activation_token.check_token(user, token)}')
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        messages.success(
            request, 'Your account has been activate successfully')
        return redirect('login')
    else:
        messages.error(
            request, 'Activation link is invalid!', extra_tags='danger')
        return redirect('login')
        # TODO: might change it later
        # return HttpResponse('Activation link is invalid!')

# @check_recaptcha
# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         logger.debug(f"email: {request.POST['email']}")
#         logger.debug(f"username: {request.POST['username']}")
#         logger.debug(f"password1: {request.POST['password1']}")
#         logger.debug(f"password2: {request.POST['password2']}")
#         if form.is_valid() and request.recaptcha_is_valid:
#             logger.debug('Form valid')
#             # TODO: Uncomment in order to save new users.
#             # form.save()
#             email = form.cleaned_data.get('email')
#             messages.success(
#                 request, f'Account for {email} has been created! You are now able to log in.')
#             return redirect('login')
#         else:
#             logger.debug('Form not valid')
#     else:
#         form = UserCreationForm()
#     return render(request, 'users/register.html', {'form': form})


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
