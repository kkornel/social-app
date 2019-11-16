from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Post


@login_required
def home(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }

    return render(request, 'social/home.html', context)
