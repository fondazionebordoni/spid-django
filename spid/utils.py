# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import get_user_model, login
from .app_settings import app_settings
from .apps import SpidConfig

# from .saml import SpidSaml2Auth

from onelogin.saml2.auth import OneLogin_Saml2_Auth


User = get_user_model()

ATTRIBUTES_MAP = {"familyName": "last_name", "name": "first_name"}


def prepare_django_request(request):
    # To handle the "multiple django projects under two sub-paths" case
    script_name = request.META.get("HTTP_X_SCRIPT_NAME", "") + request.META["PATH_INFO"]
    result = {
        "https": "on" if request.is_secure() else "off",
        "http_host": request.META["HTTP_HOST"],
        "server_port": request.META["SERVER_PORT"],
        "script_name": script_name,
        "get_data": request.GET.copy(),
        "post_data": request.POST.copy(),
    }
    if app_settings.IS_BEHIND_PROXY and "HTTP_X_FORWARDED_HOST" in request.META:
        if request.META.get("HTTP_X_FORWARDED_PROTO", "http") == "https":
            result["https"] = "on"
        else:
            result["https"] = "off"
        result["http_host"] = request.META["HTTP_X_FORWARDED_HOST"]
        result["server_port"] = request.META["HTTP_X_FORWARDED_PORT"]
    return result


def process_user(request, attributes):
    from .app_settings import app_settings

    attrs = {}
    try:
        for attr in attributes:
            if attr in app_settings.REQUESTED_ATTRIBUTES:
                key = ATTRIBUTES_MAP.get(attr, attr)
                attrs[key] = attributes[attr][0]
        user, __ = User.objects.get_or_create(**attrs)
        user.is_active = True
        login(request, user)
        return user
    except (KeyError, ValueError):
        return


def init_saml_auth(request, idp, attr_cons_index=None):
    from .app_settings import app_settings

    config = {"request_data": request}
    config["old_settings"] = SpidConfig.get_saml_settings(idp, attr_cons_index)
    auth = OneLogin_Saml2_Auth(**config)
    return auth
