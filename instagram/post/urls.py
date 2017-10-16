from django.conf.urls import url

from post import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^create/$', views.post_create, name='post_create'),
    url(r'^delete/(?P<post_pk>\d+)/$', views.post_delete, name='post_delete'),
    url(r'^comment/create/(?P<post_pk>\d+)/$', views.comment_add, name='comment_create'),
    url(r'^comment/delete/(?P<comment_pk>\d+)/$', views.comment_delete, name='comment_delete'),
]
