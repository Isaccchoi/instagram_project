from django.conf.urls import url

from post import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^create/$', views.post_add, name='post_create'),
]
