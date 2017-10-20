from django.contrib.auth import get_user_model, logout as django_logout, login as django_login
from django.shortcuts import render, redirect

from .forms import SignupForm, LoginForm

User = get_user_model()


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            django_login(request, user)
            return redirect('post:post_list')
    else:
        form = SignupForm
    context = {
        'form': form,
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
