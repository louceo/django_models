from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'header',
            'content',
            'author',
            'category',
        ]

    def clean(self):
        cleaned_data = super().clean()
        header = cleaned_data.get('header')
        content = cleaned_data.get('content')

        if header == content:
            raise ValidationError(
                'Content cannot be identical to the title name.'
            )
        if content and len(content) < 124:
            raise ValidationError(
                'Content field cannot contain less than 124 characters.'
            )
        if not content:
            raise ValidationError(
                'Content cannot be empty.'
            )
        return cleaned_data
