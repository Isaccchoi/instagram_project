from typing import NamedTuple

import requests
from django.contrib.auth import get_user_model, logout as django_logout, login as django_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from config import settings
from .forms import SignupForm, LoginForm
from .models import Relation

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
            if next_page:
                return redirect(next_page)
            return redirect('post:post_list')
    else:
        form = LoginForm
    context = {
        'form': form,
        'facebook_app_id': settings.FACEBOOK_APP_ID,
        'facebook_app_scope': settings.FACEBOOK_APP_SCOPE,
    }
    return render(request, 'member/login.html', context)


def logout(request):
    django_logout(request)
    return redirect('post:post_list')


def profile(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    my_follower = User.objects.filter(following_users=user)
    context = {
        'user': user,
        'my_follower': my_follower,
    }
    return render(request, 'member/profile.html', context)


def facebook_login(request):
    class AccessTokenInfo(NamedTuple):
        access_token: str
        token_type: str
        expires_in: str

    class DebugTokenInfo(NamedTuple):
        app_id: str
        application: str
        expires_at: int
        is_valid: bool
        issued_at: int
        scopes: list
        type: str
        user_id: str

    class UserInfo:
        def __init__(self, data):
            self.id = data['id']
            self.email = data.get('email', '')
            self.url_picture = data['picture']['data']['url']

    app_id = settings.FACEBOOK_APP_ID
    app_secret_code = settings.FACEBOOK_APP_SECRET_CODE
    app_access_token = f'{app_id}|{app_secret_code}'
    code = request.GET.get('code')

    def get_access_token_info(code):
        redirect_uri = '{scheme}://{host}{relative_url}'.format(
            scheme=request.scheme,
            host=request.META['HTTP_HOST'],
            relative_url=reverse('member:facebook_login'),
        )
        url_access_token = 'https://graph.facebook.com/v2.10/oauth/access_token'
        params_access_token = {
            'client_id': app_id,
            'redirect_uri': redirect_uri,
            'client_secret': app_secret_code,
            'code': code,
        }
        response = requests.get(url_access_token, params_access_token)
        return AccessTokenInfo(**response.json())

    def get_debug_token_info(token):
        url_debug_token = 'https://graph.facebook.com/debug_token'
        params_debug_token = {
            'input_token': token,
            'access_token': app_access_token,
        }
        response = requests.get(url_debug_token, params_debug_token)
        return DebugTokenInfo(**response.json()['data'])

    access_token_info = get_access_token_info(code)
    access_token = access_token_info.access_token
    debug_token_info = get_debug_token_info(access_token)

    params_url_user_info = {
        'fields': 'id,name,picture,email',
        'access_token': access_token,
    }
    url_user_info = 'https://graph.facebook.com/me'
    response = requests.get(url_user_info, params_url_user_info)
    result = response.json()
    user_info = UserInfo(data=result)

    username = f'fb_{user_info.id}'
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
    else:
        user = User.objects.create_user(
            user_type=User.USER_TYPE_FACEBOOK,
            username=username,
            age=0
        )
    django_login(request, user)
    return redirect('post:post_list')


@login_required
def follow_or_unfollow(request):
    if request.method != 'POST':
        return redirect('post:post_list')
    to_user = get_object_or_404(User, pk=request.POST.get('to_user'))
    from_user = request.user
    relation, created = Relation.objects.get_or_create(to_user=to_user, from_user=from_user)
    if not created:
        relation.delete()
    return redirect('member:profile', user_pk=to_user.pk)
