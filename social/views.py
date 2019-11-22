import logging

from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import (HttpResponse, HttpResponseForbidden,
                         HttpResponseRedirect)
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.views import View, generic
from django.views.generic import (
    CreateView, DeleteView, DetailView, FormView, ListView, UpdateView)
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

from users.models import MyUser, UserProfile

from .forms import CommentForm, CommentFormModal, PostForm
from .models import Comment, Like, Post

logger = logging.getLogger(__name__)


class CommentCreateViewModal(BSModalCreateView):
    model = Post
    template_name = 'social/comment_form_modal.html'
    form_class = CommentFormModal
    success_message = ''
    # success_message = 'Success: Commented.'

    def form_valid(self, form):
        # Here, unlike the solution in CommentCreateView, we have to query
        # for the post object, because it is not attached to the request.
        # So we use kwargs to get pk of that post object.
        form.instance.author = self.request.user.userprofile
        form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
        form.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


class CommentDeleteViewModal(BSModalDeleteView):
    model = Comment
    template_name = 'social/delete_comment.html'
    success_message = None
    # success_message = 'Success: Comment deleted.'
    # success_url = reverse_lazy('post-detail')

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

@login_required
def like_post(request):
    if request.method == 'POST':
        postId = request.POST.get('postId')
        userId = request.POST.get('userId')

        post = Post.objects.get(pk=int(postId))
        userprofile = UserProfile.objects.get(pk=int(userId))

        if userprofile in post.likes.all():
            post.likes.remove(userprofile)
            logger.debug('Like removed!')
            # response = f'Like removed by {userprofile.user.username}#{userprofile.user.id} for Post#{post.id}. Likes left: {post.likes.count()}'
        else:
            post.likes.add(userprofile)
            logger.debug('Like added!')
            # response = f'Like number {post.likes.count()} added for Post#{post.id} by {userprofile.user.username}#{userprofile.user.id}'

        #  TODO remove after testing with multiple users
        logger.debug(
            f'### {userprofile.user.username}\'s likes: #######################')
        for e in userprofile.likes.all():
            logger.debug(' - ' + str(e))
        logger.debug(f'### {post} likes: #######################')
        for e in post.likes.all():
            logger.debug(' - ' + str(e))

        logger.debug('### All likes: #######################')
        for e in Like.objects.all():
            logger.debug(' - ' + str(e))
    response = post.likes.all().count()
    return HttpResponse(response)


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class CommentCreateView(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = Post
    form_class = CommentForm
    template_name = 'social/post_detail.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.userprofile
        form.instance.post = self.object
        form.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})


class PostDetail(View):
    """https://docs.djangoproject.com/en/2.2/topics/class-based-views/mixins/#using-formmixin-with-detailview"""

    def get(self, request, *args, **kwargs):
        view = PostDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentCreateView.as_view()
        return view(request, *args, **kwargs)


class UserProfileView(ListView):
    model = Post
    template_name = 'social/user_profile.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = MyUser.objects.get(username=self.kwargs.get('username'))
        userprofile = get_object_or_404(UserProfile, user=user)
        return Post.objects.filter(author=userprofile).order_by('-date_posted')


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
        form.instance.author = self.request.user.userprofile
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    # Specifying both 'fields' and 'form_class' is not permitted.
    form_class = PostForm
    # Either form_class or fields
    # fields = ['content', 'location', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user.userprofile
        return super().form_valid(form)

    def test_func(self):
        """
        This function is run by UserPassesTestMixin to check something that we want to check.
        In this case we want to check if the currently logged in user is also the author of the post.
        If he is not, then he has no permissions to do that.
        """
        post = self.get_object()
        return self.request.user.userprofile == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    context_object_name = 'post'
    success_url = '/'  # Where to go after deleting.

    def test_func(self):
        post = self.get_object()
        return self.request.user.userprofile == post.author


@login_required
def home(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'social/home.html', context)
