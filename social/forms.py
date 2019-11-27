import logging

from bootstrap_modal_forms.forms import BSModalForm
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
    # If using CrispyForms, the only way to change background of textarea
    # is to define style here. With CSS selector it's not working.
    text = forms.CharField(max_length=280, label='', widget=forms.Textarea(attrs={
        'rows': 3,
        'cols': 10,
        # 'style': 'resize:none;',
        'style': 'resize:none; background-color: #000000; color: #d9d9d9;',
        'placeholder': 'Leave your comment',
    }))

    class Meta:
        model = Comment
        fields = ['text']
        # widgets = {'text': forms.Textarea(attrs={'placeholder': 'Comment this post'}), }


class CommentFormModal(BSModalForm):
    text = forms.CharField(max_length=280, label='', widget=forms.Textarea(attrs={
        'rows': 4,
        # 'cols': 30,
        'style': 'resize:none;',
        'placeholder': 'Leave your feedback',
    }))

    class Meta:
        model = Comment
        fields = ['text']


class PostFormModal(BSModalForm):
    # If using CrispyForms, the only way to change background of textarea
    # is to define style here. With CSS selector it's not working.
    content = forms.CharField(max_length=280, widget=forms.Textarea(attrs={
        'rows': 4,
        # 'cols': 30,
        # 'style': 'resize:none;',
        'style': 'resize:none; background-color: #15181c; color: #d9d9d9;',
        'placeholder': 'Text of your post',
    }))
    # To remove 'Currently photo' and 'Clear' field,
    # use this after required: widget=forms.FileInput
    image = forms.ImageField(
        label='Change current image for new one:', required=False, widget=forms.FileInput)

    delete_current_image = forms.BooleanField(label='or only delete current (checkbox):',
                                              required=False)

    class Meta:
        model = Post
        fields = ['content', 'location', 'image']
