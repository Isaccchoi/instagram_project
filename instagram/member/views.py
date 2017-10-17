from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

from .forms import UserForm
User = get_user_model()


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            if not User.objects.filter(username=form.cleaned_data['username']).exists():
                User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        context = {
            'user_form': UserForm
        }
    else:
        context = {
            'user_form': UserForm,
        }
    return render(request, 'member/signup.html', context)


def login_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('post:post_list')
    else:
        form = UserForm
    context = {
        'user_form': form,
    }
    return render(request, 'member/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('post:post_list')
