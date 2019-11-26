import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .admin import UserCreationForm
from .decorators import check_recaptcha, func_log
from .forms import (CaptchaPasswordResetForm, MyUserUpdateForm,
                    UserProfileUpdateForm)
from .models import MyUser, UserProfile
from .tokens import account_activation_token

# from app.models import Model


logger = logging.getLogger(__name__)


@func_log
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

            # Password confirmation.
            user = form.save(commit=False)
            user.is_active = False
            # TODO: Uncomment in order to save new users.
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Account - Django Social App'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)

            logger.debug(f'uid: {uid}')
            logger.debug(f'token: {token}')
            logger.debug(f'user: {user}')

            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })

            to_email = form.cleaned_data.get('email')

            send_mail(
                subject,
                message,
                'from@example.com',
                [to_email],
                fail_silently=False,
                html_message=message
            )

            messages.info(
                request, f'Confirmation email has been sent to {to_email}')
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
        logger.debug(f'user: {user}')
    except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, 'Your account has been activated successfully. You are now able to log in.')
        return redirect('login')
    else:
        messages.error(
            request, 'Activation link is invalid!', extra_tags='danger')
        return redirect('login')
        # TODO: might change it later
        # return HttpResponse('Activation link is invalid!')


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


@login_required
def userprofile(request):
    if request.method == "POST":
        myuser_form = MyUserUpdateForm(request.POST,
                                       instance=request.user)
        profile_form = UserProfileUpdateForm(request.POST,
                                             request.FILES,
                                             instance=request.user.userprofile)

        if myuser_form.is_valid() and profile_form.is_valid():
            myuser_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        myuser_form = MyUserUpdateForm(instance=request.user)
        profile_form = UserProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'myuser_form': myuser_form,
        'profile_form': profile_form,
    }

    return render(request, 'users/edit_profile.html', context)


@login_required
def edit_userprofile(request):
    if request.method == "POST":
        myuser_form = MyUserUpdateForm(request.POST,
                                       instance=request.user)
        profile_form = UserProfileUpdateForm(request.POST,
                                             request.FILES,
                                             instance=request.user.userprofile)

        if myuser_form.is_valid() and profile_form.is_valid():
            status = profile_form.cleaned_data['delete_current_image']
            logger.debug(status)
            myuser_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        myuser_form = MyUserUpdateForm(instance=request.user)
        profile_form = UserProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'myuser_form': myuser_form,
        'profile_form': profile_form,
    }

    return render(request, 'users/edit_profile_modal.html', context)
