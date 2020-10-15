# -*- coding: utf-8 -*-
import os
from django.http import FileResponse
from django.urls import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView
from spid.utils import is_user_authenticated
from .settings import BASE_DIR

class IndexView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_logged_in'] =  is_user_authenticated(self.request)
        return context

def attrs(request):
    paint_logout = False
    attributes = False

    if 'samlUserdata' in request.session:

        paint_logout = True
        if len(request.session['samlUserdata']) > 0:
            attributes = request.session['samlUserdata'].items()

    return render_to_response('attrs.html',
                              context=RequestContext(
                                    request,
                                    {
                                        'is_logged_in': is_user_authenticated(request),
                                        'paint_logout': paint_logout,
                                        'attributes': attributes
                                    }
                             ).flatten()
    )

def metadata(request):
    """
        Expose SP Metadata
    """
    metadata_file = os.path.join(BASE_DIR, 'spid-sp-metadata', 'metadata.xml')
    if os.path.exists(metadata_file):
        data = open(metadata_file, 'rb')
        response = FileResponse(data, content_type='text/xml')
        return response
    else:
        return render_to_response('No metadata found in {}'.format(metadata_file))
