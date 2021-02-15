# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import RequestContext
from django.views.decorators.http import require_POST, require_http_methods
from .utils import init_saml_auth, prepare_django_request
from onelogin.saml2.settings import OneLogin_Saml2_Settings
from onelogin.saml2.utils import OneLogin_Saml2_Utils
from datetime import datetime, timezone


def login(request):
    """
    Handle login action ( SP -> IDP )
    """
    # Post-login activity
    if "samlUserdata" in request.session:
        after_login_redirect_url = "/"
        if settings.SPID_POST_LOGIN_URL:
            after_login_redirect_url = reverse(settings.SPID_POST_LOGIN_URL)
        if "next" in request.session:
            after_login_redirect_url = "%s?next=%s" % (after_login_redirect_url, request.session["next"])
            del request.session["next"]
        return HttpResponseRedirect(after_login_redirect_url)

    # Pre-login
    req = prepare_django_request(request)
    if "idp" in req["get_data"]:
        idp = req["get_data"].get("idp")
        request.session["idp"] = idp
        attr_cons_index = req["get_data"].get("index")
        auth = init_saml_auth(req, idp, attr_cons_index)
        args = []
        if "next" in req["get_data"]:
            request.session["next"] = req["get_data"].get("next")
            # args.append(req["get_data"].get("next"))
        redirect_url = auth.login(return_to="/spid/spid-login", force_authn=True, *args)
        request.session["request_id"] = auth.get_last_request_id()
        request.session["request_instant"] = datetime.now(timezone.utc).timestamp()
        request.session["attr_cons_index"] = attr_cons_index
        return HttpResponseRedirect(redirect_url)
    else:
        print("------- ERROR: not IDP in session!")
        return redirect(settings.SPID_BAD_REQUEST_REDIRECT_PAGE)


def slo_logout(request):
    """
    Logout
    Handle SLO ( SP -> IDP )
    """
    req = prepare_django_request(request)
    idp = request.session.get("idp")
    if idp and idp in settings.SPID_IDP_NAME_QUALIFIERS.keys():
        auth = init_saml_auth(req, idp)
        name_id = None
        session_index = None
        if "samlNameId" in request.session:
            name_id = request.session["samlNameId"]
        if "samlSessionIndex" in request.session:
            session_index = request.session["samlSessionIndex"]
        idp_name_qualifier = settings.SPID_IDP_NAME_QUALIFIERS[idp]
        redirect_url = auth.logout(
            name_id=name_id,
            session_index=session_index,
            return_to="/spid/slo-logout/",
            # TODO capire come deve essere
            # Da regole tecniche: NameQualifier che qualifica il dominio a cui afferisce tale valore
            # (URI riconducibile alla stessa entità emittente) => va bene l'entityID?;
            nq=idp_name_qualifier,
        )
        request.session["request_id"] = auth.get_last_request_id()
        return HttpResponseRedirect(redirect_url)
    else:
        if not idp:
            print("------- ERROR: not IDP in session!")
        if idp not in settings.SPID_IDP_NAME_QUALIFIERS.keys():
            print("------- ERROR: bad IDP value! '%s'" % (idp))
        # Return to homepage
        return redirect(settings.SPID_BAD_REQUEST_REDIRECT_PAGE)


@csrf_exempt
def sls_logout(request):
    """
    Logout
    Handle SLS ( IDP -> SP )
    """
    req = prepare_django_request(request)
    idp = request.session.get("idp")
    request_id = request.session.get("request_id")
    if idp and request_id:
        auth = init_saml_auth(req, idp)
        # TODO maybe just remove the SPID data from the session
        # TODO the callback is not being called!
        dscb = lambda: request.session.flush()
        url = auth.process_slo(delete_session_cb=dscb, request_id=request_id)
        errors = auth.get_errors()
        if len(errors) > 0:
            # Redirect to error page
            error_params = "?errors=%s&error_msg=%s" % (
                errors,
                auth.get_last_error_reason(),
            )
            return redirect(reverse(settings.SPID_ERROR_PAGE_URL) + error_params)
        # If there was no error, logout the user and redirect him/her to the homepage (or whather URL was selected)
        redirect_to = reverse(settings.SPID_POST_LOGOUT_URL)
        if url is not None:
            redirect_to = url
        else:
            django_logout(request)
        return HttpResponseRedirect(redirect_to)
    else:
        if not idp:
            print("------- ERROR: not IDP in session!")
        if idp not in settings.SPID_IDP_NAME_QUALIFIERS.keys():
            print("------- ERROR: bad IDP value! '%s'" % (idp))
        if not request_id:
            print("------- ERROR: no request ID!")
        # Return to homepage
        return redirect(settings.SPID_BAD_REQUEST_REDIRECT_PAGE)


@csrf_exempt
def attributes_consumer(request):
    """
    Consume attributes from IDP
    ( IDP -> SP )
    """
    req = prepare_django_request(request)
    idp = request.session.get("idp")
    attr_cons_index = request.session.get("attr_cons_index")
    request_id = request.session.get("request_id")
    request_instant = request.session.get("request_instant")
    if idp and request_id:
        auth = init_saml_auth(req, idp, attr_cons_index)
        errors = []
        auth.process_response(request_id=request_id, request_instant=request_instant)
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
