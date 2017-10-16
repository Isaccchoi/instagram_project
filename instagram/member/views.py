from django.contrib.auth.models import User
from django.shortcuts import render

from .forms import UserForm


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        context = {
            'user_form': UserForm
        }
    else:
        context = {
            'user_form': UserForm,
        }
    return render(request, 'member/signup.html', context)
