import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView)

from users.models import Profile

from .forms import PostForm
from .models import Post

logger = logging.getLogger(__name__)


def like_post(request):
    from django.conf import settings as ds
    from social_app import settings as ms

    logger.debug(ds.AUTH_USER_MODEL)
    logger.debug(ms.AUTH_USER_MODEL)
    logger.debug(request.method)

    if request.method == 'POST':
        foo = request.POST.get('postId')
        bar = request.POST.get('userId')
        post = Post.objects.get(pk=int(foo))
        logger.debug(post)
        user = Profile.objects.get(pk=int(bar))
        logger.debug(user)
        post.likes.add(user)

        # for e in user:
        #     logger.debug(e)

        for e in user.post_likes.all():
            logger.debug(e)

        for e in post.likes.all():
            logger.debug(e)

    else:
        foo = request.GET.get('postId')
        bar = request.GET.get('userId')

    logger.debug(foo)
    logger.debug(bar)

    return HttpResponse('')


class UserProfilePostsView(ListView):
    model = Post
    template_name = 'social/user_profile_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(MyUser, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostListView(ListView):
    model = Post
    # If not specified, Django looks for template in following path: '<app>/<model>_<viewtype>.html'
    template_name = 'social/home.html'
    # If not specified, Django uses name 'object' for data passed to template file.
    context_object_name = 'posts'
    ordering = ['-date_posted']
    # paginate_by = 5


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    # Specifying both 'fields' and 'form_class' is not permitted.
    form_class = PostForm
    # Either form_class or fields.
    # fields = ['content', 'location', 'image']
    # We do not have to specify template_name, because Django uses post_form.html,
    # for both: CreateView and UpdateView. No need to create seperate.
    # template_name = 'social/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    # Specifying both 'fields' and 'form_class' is not permitted.
    form_class = PostForm
    # Either form_class or fields
    # fields = ['content', 'location', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """
        This function is run by UserPassesTestMixin to check something that we want to check.
        In this case we want to check if the currently logged in user is also the author of the post.
        If he is not, then he has no permissions to do that.
        """
        post = self.get_object()
        return self.request.user == post.author


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    context_object_name = 'post'
    success_url = '/'  # Where to go after deleting.

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


@login_required
def home(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'social/home.html', context)
