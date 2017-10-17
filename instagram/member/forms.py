from django import forms


class UserForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(
        widget=forms.PasswordInput,
    )