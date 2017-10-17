from django.contrib.auth import get_user_model, authenticate, login as django_login, logout as django_logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import UserForm

User = get_user_model()


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


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(
            username=username,
            password=password
        )
        if user is not None:
            django_login(request, user)
            return redirect('post:post_list')
        else:
            return HttpResponse('Login credentials invalid')
    else:
        return render(request, 'member/login.html')


def logout(request):
    django_logout(request)
    return redirect('post:post_list')
