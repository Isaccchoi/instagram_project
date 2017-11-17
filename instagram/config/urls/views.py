from django.conf.urls import url, include
from django.contrib import admin

from config import views
from member.urls import views as member_urls
from member.apis import FacebookLogin
from post import urls as post_urls
from sms import urls as sms_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^post/', include(post_urls, namespace='post')),
    url(r'^member/', include(member_urls, namespace='member')),
    url(r'^facebook-login/$', FacebookLogin.as_view(), name='api-facebook'),
    url(r'^sms/', include(sms_urls, namespace='sms')),

]
