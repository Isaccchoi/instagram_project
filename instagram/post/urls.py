from django.conf.urls import url

from post import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post_create/$', views.post_add, name='post_create'),
    url(r'^post_delete/(?P<post_pk>\d+)/$', views.post_delete, name='post_delete'),
    url(r'^comment_create/(?P<post_pk>\d+)/$', views.comment_add, name='comment_create'),
    url(r'^comment_delete/(?P<comment_pk>\d+)/$', views.comment_delete, name='comment_delete'),
]
