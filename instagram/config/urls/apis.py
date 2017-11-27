from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token

from member.apis import Login, Signup
from post.apis import PostListView

urlpatterns = [
    url(r'^token-auth/$', obtain_auth_token, name='auth-token'),
    url(r'^post/$', PostListView.as_view(), name='api-post'),
    url(r'^member/login/$', Login.as_view(), name='api-login'),
    url(r'^member/signup/$', Signup.as_view(), name='api-signup'),
]
