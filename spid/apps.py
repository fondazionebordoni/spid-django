# -*- coding: utf-8 -*-
import pkg_resources
import os
from xml.etree import ElementTree as et
from django.conf import settings
from django.apps import AppConfig

from .app_settings import app_settings


def get_idp_config(id, name=None):
    xml_path = os.path.join(app_settings.IDP_METADATA_DIR, 'spid-idp-%s.xml' % id)
    idp_metadata = et.parse(xml_path).getroot()
    sso_path = './/{%s}SingleSignOnService[@Binding="%s"]' % (
        app_settings.SAML_METADATA_NAMESPACE,
        app_settings.BINDING_REDIRECT_URN,
    )
    slo_path = './/{%s}SingleLogoutService[@Binding="%s"]' % (
        app_settings.SAML_METADATA_NAMESPACE,
        app_settings.BINDING_REDIRECT_URN,
    )

    try:
        sso_location = idp_metadata.find(sso_path).attrib["Location"]
    except (KeyError, AttributeError) as err:
        raise ValueError("Missing metadata SingleSignOnService for %r: %r" % (id, err))

    try:
        slo_location = idp_metadata.find(slo_path).attrib["Location"]
    except (KeyError, AttributeError) as err:
        raise ValueError("Missing metadata SingleLogoutService for %r: %r" % (id, err))

    return {
        "name": name,
        "idp": {
            "entityId": idp_metadata.get("entityID"),
            "singleSignOnService": {
                "url": sso_location,
                "binding": app_settings.BINDING_REDIRECT_URN,
            },
            "singleLogoutService": {
                "url": slo_location,
                "binding": app_settings.BINDING_REDIRECT_URN,
            },
            "x509cert": idp_metadata.find(
                ".//{%s}X509Certificate" % app_settings.XML_SIGNATURE_NAMESPACE
            ).text,
        },
    }


class SpidConfig(AppConfig):
    name = "spid"
    verbose_name = "SPID Authentication"

    identity_providers_spid = {
        id: get_idp_config(id, name) for id, name in app_settings.IDENTITY_PROVIDERS
    }

    identity_providers = identity_providers_spid.copy()
    identity_providers.update({
        id: get_idp_config(id, name) for id, name in app_settings.IDENTITY_PROVIDERS_EID
    })

    @staticmethod
    def get_saml_settings(idp_id, attr_cons_index=None):
        saml_settings = dict(app_settings.config)
        saml_settings.update({"idp": SpidConfig.identity_providers[idp_id]["idp"]})
        if attr_cons_index:
            saml_settings["sp"]["attributeConsumingServiceIndex"] = attr_cons_index
        return saml_settings
