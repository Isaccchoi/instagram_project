from django.conf.urls import url

from .. import apis

urlpatterns = [
    url(r'^api/', apis.PostListView.as_view(), name='post_api_list'),
    url(r'^api/(?P<post_pk>\d+)/$', apis.PostDetailView.as_view(), name='post_api_list'),
]
