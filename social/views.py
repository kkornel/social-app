from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import CreateView, ListView

from .models import Post


class PostCreateView(CreateView):
    model = Post
    fields = ['content', 'location', 'image']
    # template_name = 'social/home.html'


class PostListView(ListView):
    model = Post
    # If not specified, Django looks for template in following path: '<app>/<mode>_<viewtype>.html'
    template_name = 'social/home.html'
    # If not specified, Django uses name 'object' for data in template file.
    context_object_name = 'posts'
    ordering = ['-date_posted']


@login_required
def home(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }

    return render(request, 'social/home.html', context)
