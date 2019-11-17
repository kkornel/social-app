import logging

from django import forms

from .models import Post

logger = logging.getLogger(__name__)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'location', 'image']
        widgets = {'content': forms.Textarea(attrs={'rows': 3,
                                                    'cols': 10,
                                                    'style': 'resize:none;',
                                                    'placeholder': 'What are you up to?'}),
                   'location': forms.TextInput(attrs={'placeholder': 'e.g. Stockholm, Sweden'}),
                   }
