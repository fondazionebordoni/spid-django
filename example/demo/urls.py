# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from .views import IndexView, attrs, metadata
admin.autodiscover()


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^metadata/', metadata, name='metadata'),
    url(r'^attrs/$', attrs, name='attrs'),
    url(r'^spid/', include('spid.urls')),
    url(r'^$', IndexView.as_view(), name='index'),
]
