# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from .views import IndexView, AttrsView, metadata, ErrorPageView

admin.autodiscover()


urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^metadata/", metadata, name="metadata"),
    url(r"^attrs/$", AttrsView.as_view(), name="attrs"),
    url(r"^errors/$", ErrorPageView.as_view(), name="errors"),
    url(r"^spid/", include("spid.urls")),
    url(r"^$", IndexView.as_view(), name="index"),
]
