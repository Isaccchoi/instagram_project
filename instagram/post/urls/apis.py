from django.conf.urls import url

from .. import apis

urlpatterns = [
    url(r'^$', apis.PostListView.as_view(), name='post-list'),
    url(r'^(?P<pk>\d+)/like-toggle/$', apis.PostListView.as_view(), name='post-list'),
]