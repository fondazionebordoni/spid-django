# -*- coding: utf-8 -*-
import ast
import os
from django.http import FileResponse
from django.urls import reverse
from django.shortcuts import redirect, render
from django.template import RequestContext
from django.views.generic import TemplateView
from .settings import SAML_FOLDER, SPID_IS_BEHIND_PROXY


class IndexView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        if SPID_IS_BEHIND_PROXY and 'HTTP_X_FORWARDED_HOST' in self.request.META:
            print(self.request.META)
        context = super().get_context_data(**kwargs)
        context["is_logged_in"] = "samlUserdata" in self.request.session
        return context


class AttrsView(TemplateView):

    template_name = "attrs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paint_logout = False
        attributes = False
        is_logged_in = False
        if "samlUserdata" in request.session:
            is_logged_in = True
            paint_logout = True
            if len(request.session["samlUserdata"]) > 0:
                attributes = request.session["samlUserdata"].items()
        context["is_logged_in"] = is_logged_in
        context["paint_logout"] = paint_logout
        context["attributes"] = attributes
        return context


def metadata(request):
    """
    Expose SP Metadata
    """
    metadata_file = os.path.join(SAML_FOLDER, "spid-sp-metadata", "metadata.xml")
    if os.path.exists(metadata_file):
        data = open(metadata_file, "rb")
        response = FileResponse(data, content_type="text/xml")
        return response
    else:
        return render(request, "No metadata found in {}".format(metadata_file))


class ErrorPageView(TemplateView):
    template_name = "errors.html"

    def dispatch(self, request, *args, **kwargs):
        result = super().dispatch(request, *args, **kwargs)
        if "errors" not in self.request.GET or "error_msg" not in self.request.GET:
            return redirect(reverse("index"))
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        errors = ast.literal_eval(self.request.GET.get("errors", None))
        context["errors"] = errors
        context["error_msg"] = self.request.GET.get("error_msg", None)
        return context
