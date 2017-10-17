from django.contrib.auth import get_user_model, logout as django_logout
from django.shortcuts import render, redirect

from .forms import UserForm, LoginForm

User = get_user_model()


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.signup(request)
            return redirect('post:post_list')
    else:
        form = UserForm
    context = {
        'user_form': form,
    }
    return render(request, 'member/signup.html', context)


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            return redirect('post:post_list')
    else:
        form = LoginForm
    context = {
        'form': form
    }
    return render(request, 'member/login.html', context)


def logout(request):
    django_logout(request)
    return redirect('post:post_list')
