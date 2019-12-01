import logging

from bootstrap_modal_forms.generic import BSModalUpdateView
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.files import File
from django.core.files.storage import default_storage as storage
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import ListView, UpdateView

from social.models import Post

from .admin import UserCreationForm
from .decorators import check_recaptcha, func_log
from .forms import (CaptchaPasswordResetForm, CustomChangePasswordForm,
                    MyUserUpdateForm, MyUserUpdateFormModal,
                    UserProfileUpdateForm, UserProfileUpdateFormModal)
from .models import MyUser, UserProfile
from .tokens import account_activation_token

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
@check_recaptcha
def password_change(request):
    if request.method == 'POST':
        form = CustomChangePasswordForm(data=request.POST, user=request.user)
        if form.is_valid() and request.recaptcha_is_valid:
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password changed.')
            return redirect('profile', username=request.user.username)
    else:
        form = CustomChangePasswordForm(user=request.user)
    return render(request, 'users/password_change.html', {'form': form})


class UserProfileDetailListView(ListView):
    """https://stackoverflow.com/questions/41287431/django-combine-detailview-and-listview"""
    detail_context_object_name = 'userprofile'
    model = Post
    template_name = 'users/profile.html'
    context_object_name = 'posts'
    # paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(UserProfileDetailListView, self).get(request, *args, **kwargs)

    def get_object(self):
        username = self.kwargs.get('username')
        user = MyUser.objects.get(username=username)
        return get_object_or_404(UserProfile, user=user)

    def get_queryset(self):
        return Post.objects.filter(author=self.object).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super(UserProfileDetailListView,
                        self).get_context_data(**kwargs)
        context[self.detail_context_object_name] = self.object
        return context


class MyUserUpdateViewModal(BSModalUpdateView):
    model = MyUser
    template_name = 'users/profile_edit_modal.html'
    form_class = MyUserUpdateFormModal
    # success_message = 'Email successfully changed.'
    success_message = ''
    # success_url = '/profile'

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


class UserProfileUpdateViewModal(BSModalUpdateView):
    model = UserProfile
    template_name = 'users/profile_edit_modal.html'
    form_class = UserProfileUpdateFormModal
    # success_message = 'Profile successfully updated.'
    success_message = ''
    # success_url = '/profile'

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

    def form_valid(self, form):
        # TODO Still no idea how to replace with default.
        logger.debug('form_valid')
        delete_current_image = form.cleaned_data['delete_current_image']
        image = form.cleaned_data['image']
        logger.debug(image)
        logger.debug(type(image))
        logger.debug(delete_current_image)
        if delete_current_image:
            userprofile = self.request.user.userprofile
            current_image = userprofile.image
            if current_image.name != 'default.jpg':
                logger.debug("current_image.name != 'default.jpg'")
                userprofile.image.delete(save=False)
                logger.debug("deleted old")
                new = storage.open('default.jpg').read()
                # logger.debug(new)
                logger.debug(type(new))
                filee = File(new)
                # logger.debug(filee)
                logger.debug(type(filee))
                userprofile.image.save('default.jpg', filee)
                logger.debug('lil')
        return super().form_valid(form)


# Used this to have two forms in one view.
# Firstly I had a templte using this view,
# but I went with modals, so not using it currently.
# Leaving for future.
@login_required
def edit_userprofile(request):
    if request.method == "POST":
        myuser_form = MyUserUpdateForm(request.POST,
                                       instance=request.user)
        profile_form = UserProfileUpdateForm(request.POST,
                                             request.FILES,
                                             instance=request.user.userprofile)

        if myuser_form.is_valid() and profile_form.is_valid():
            # TODO delete img.
            # TODO update with solution from CBS from above
            delete_current_image = profile_form.cleaned_data['delete_current_image']
            logger.debug(delete_current_image)
            if delete_current_image:
                userprofile = request.user.userprofile
                current_image = userprofile.image
                if current_image.name != 'default.jpg':
                    logger.debug("current_image.name != 'default.jpg'")
                    userprofile.image.delete(save=False)
                    logger.debug("deleted old")
                    new = storage.open('default.jpg').read()
                    logger.debug(new)
                    logger.debug(type(new))
                    filee = File(new)
                    logger.debug(filee)
                    logger.debug(type(filee))
                    # userprofile.image.save('default.jpg', filee)
                    logger.debug('lil')
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

    return render(request, 'users/profile_edit_modal.html', context)
