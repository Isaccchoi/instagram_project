from django.conf.urls import url, include

from .. import apis, views

urlpatterns = [
    url(r'^api', include(apis), name='api'),
    url(r'^', include(views), name='views'),
]
