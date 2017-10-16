from django import forms


class PostForm(forms.Form):
    photo = forms.ImageField(required=True)
    text = forms.CharField(max_length=5)

    def clean_text(self):
        data = self.cleaned_data['text']
        if data != data.upper():
            raise forms.ValidationError('All text must uppercase!')


class PostCommentForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        ),
    )