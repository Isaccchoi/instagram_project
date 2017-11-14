from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from ..urls import apis, views

urlpatterns = [
    url(r'^api/', include(apis, namespace='apis')),
    url(r'^', include(views, namespace='views')),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
