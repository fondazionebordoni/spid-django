# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import RequestContext
from django.views.decorators.http import require_POST, require_http_methods
from .utils import init_saml_auth, prepare_django_request
from onelogin.saml2.settings import OneLogin_Saml2_Settings
from onelogin.saml2.utils import OneLogin_Saml2_Utils


def login(request):
    """
    Handle login action ( SP -> IDP )
    """
    if "samlUserdata" in request.session:
        return HttpResponseRedirect("/")
    req = prepare_django_request(request)
    if "idp" in req["get_data"]:
        idp = req["get_data"].get("idp")
        request.session["idp"] = idp
        attr_cons_index = req["get_data"].get("index")
        auth = init_saml_auth(req, idp, attr_cons_index)
        args = []
        if "next" in req["get_data"]:
            args.append(req["get_data"].get("next"))
        redirect_url = auth.login(*args)
        request.session["request_id"] = auth.get_last_request_id()
        request.session["attr_cons_index"] = attr_cons_index
        return HttpResponseRedirect(redirect_url)
    return HttpResponseServerError()


def slo_logout(request):
    """
    Logout
    Handle SLO ( SP -> IDP )
    """
    req = prepare_django_request(request)
    idp = request.session.get("idp")
    if idp:
        auth = init_saml_auth(req, idp)
        name_id = None
        session_index = None
        if "samlNameId" in request.session:
            name_id = request.session["samlNameId"]
        if "samlSessionIndex" in request.session:
            session_index = request.session["samlSessionIndex"]
        return HttpResponseRedirect(
            auth.logout(
                name_id=name_id,
                session_index=session_index,
                # TODO capire come deve essere
                nq="dummyvalue",
            )
        )
    return HttpResponseServerError()


def sls_logout(request):
    """
    Logout
    Handle SLS ( IDP -> SP )
    """
    req = prepare_django_request(request)
    idp = request.session.get("idp")
    if idp:
        auth = init_saml_auth(req, idp)
        # TODO maybe just remove the SPID data from the session
        # TODO the callback is not being called!
        dscb = lambda: request.session.flush()
        url = auth.process_slo(delete_session_cb=dscb)
        errors = auth.get_errors()
        if len(errors) > 0:
            return HttpResponseServerError(errors)
        redirect_to = "/"
        if url is not None:
            redirect_to = url
        else:
            django_logout(request)
        return HttpResponseRedirect(redirect_to)
    return HttpResponseServerError()


def attributes_consumer(request):
    """
    Consume attributes from IDP
    ( IDP -> SP )
    """
    req = prepare_django_request(request)
    idp = request.session.get("idp")
    attr_cons_index = request.session.get("attr_cons_index")
    request_id = request.session.get("request_id")
    if idp and request_id:
        auth = init_saml_auth(req, idp, attr_cons_index)
        errors = []
        auth.process_response(request_id=request_id)
        errors = auth.get_errors()
        if not errors:
            user_attributes = auth.get_attributes()
            request.session["samlUserdata"] = user_attributes
            request.session["samlNameId"] = auth.get_nameid()
            request.session["samlSessionIndex"] = auth.get_session_index()
            redirect_to = "/"
            if (
                "RelayState" in req["post_data"]
                and OneLogin_Saml2_Utils.get_self_url(req)
                != req["post_data"]["RelayState"]
            ):
                redirect_to = auth.redirect_to(req["post_data"]["RelayState"])
            return HttpResponseRedirect(redirect_to)
        else:
            error_params = "?errors=%s&error_msg=%s" % (
                errors,
                auth.get_last_error_reason(),
            )
            return redirect(reverse(settings.SPID_ERROR_PAGE_URL) + error_params)
    else:
        if not idp:
            print("------- ERROR: not IDP in session!")
        if not request_id:
            print("------- ERROR: not request_id in session!")
        # Return to homepage
        return redirect(settings.SPID_BAD_REQUEST_REDIRECT_PAGE)
