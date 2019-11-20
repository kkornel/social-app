import logging

from django import forms

from .models import Comment, Post

logger = logging.getLogger(__name__)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'location', 'image']
        widgets = {'content': forms.Textarea(attrs={
            'rows': 3,
            'cols': 10,
            'style': 'resize:none;',
            'placeholder': 'What are you up to?',
        }),
            'location': forms.TextInput(attrs={
                'placeholder': 'e.g. Stockholm, Sweden',
            }),
        }


class CommentForm(forms.ModelForm):
    text = forms.CharField(label='', widget=forms.Textarea(attrs={
        'rows': 3,
        'cols': 10,
        'style': 'resize:none;',
        'placeholder': 'Leave your replay',
    }),
    )

    class Meta:
        model = Comment
        fields = ['text']
        # widgets = {'text': forms.Textarea(attrs={'placeholder': 'Comment this post'}), }
