from django import forms

from .models import Post, PostComment


class PostForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['author'].required = True

    class Meta:
        model = Post
        fields = ('photo',)
        widgets = {
            'photo': forms.FileInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }

    def save(self, commit=True, *args, **kwargs):
        if not self.instance.pk and commit:
            author = kwargs.pop('author', None)
            if not author:
                raise ValueError('Author field is required')
            self.instance.author = author
        return super().save(*args, **kwargs)


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ('content',)
        widgets = {
            'content': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }