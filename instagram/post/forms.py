from django import forms


class PostForm(forms.Form):
    photo = forms.ImageField(label="사진")
