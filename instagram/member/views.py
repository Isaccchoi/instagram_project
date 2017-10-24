from pprint import pprint

import requests
from django.contrib.auth import get_user_model, logout as django_logout, login as django_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from config import settings
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
    next_page = request.GET.get('next')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            return redirect(next_page)
    else:
        form = LoginForm
    context = {
        'form': form,
        'facebook_app_id': settings.FACEBOOK_APP_ID,
    }
    return render(request, 'member/login.html', context)


def logout(request):
    django_logout(request)
    return redirect('post:post_list')


@login_required
def profile(request):
    return HttpResponse(f'{request.user.user_name} profile')


def facebook_login(request):
    app_id = settings.FACEBOOK_APP_ID
    app_secret_code = settings.FACEBOOK_APP_SECRET_CODE
    code = request.GET.get('code')
    redirect_uri = '{scheme}://{host}{relative_url}'.format(
        scheme=request.scheme,
        host=request.META['HTTP_HOST'],
        relative_url=reverse('member:facebook_login'),
    )
    print('redirect_uri:', redirect_uri)
    url_access_token = 'https://graph.facebook.com/v2.10/oauth/access_token'
    params_access_token = {
        'client_id': app_id,
        'redirect_uri': redirect_uri,
        'client_secret': app_secret_code,
        'code': code,
    }
    response = requests.get(url_access_token, params_access_token)
    result = response.json()
    pprint(result)
    return HttpResponse(result)

    # if request.GET.get('code'):

    #     redirect_uri = "http://localhost:8000/" + reverse('member:facebook_login')
    #     print(redirect_uri)

    #     code_parameter = request.GET.get('code')
    #     r = requests.get(f"https://graph.facebook.com/v2.10/oauth/access_token?client_id={app_id}"
    #                      f"&redirect_uri={redirect_uri}"
    #                      f"&client_secret={app_secret}"
    #                      f"&code={code_parameter}")
