# -*- coding: utf-8 -*-
from django.conf import settings

class AppSettings(object):

    def __init__(self, prefix):
        self.prefix = prefix

    def _setting(self, name, default_value):
        return getattr(settings, self.prefix + name, default_value)

    @property
    def IDP_METADATA_DIR(self):
        return self._setting('IDP_METADATA_DIR', [])

    @property
    def IDENTITY_PROVIDERS(self):
        return self._setting('IDENTITY_PROVIDERS', [])

    @property
    def SP_DOMAIN(self):
        return self._setting('SP_DOMAIN', 'https://spid.test.it:8000')

    @property
    def SP_ENTITY_ID(self):
        return self._setting('SP_ENTITY_ID', self.SP_DOMAIN)

    @property
    def SP_ASSERTION_CONSUMER_SERVICE(self):
        return self._setting('SP_ASSERTION_CONSUMER_SERVICE', '{0}/{1}'.format(self.SP_DOMAIN, 'assertion-consumer'))

    @property
    def SP_SINGLE_LOGOUT_SERVICE(self):
        return self._setting('SP_SINGLE_LOGOUT_SERVICE', '{0}/{1}'.format(self.SP_DOMAIN, 'single-logout'))

    @property
    def SP_ATTRIBUTE_CONSUMING_SERVICE_INDEX(self):
        return self._setting('SP_ATTRIBUTE_CONSUMING_SERVICE_INDEX', "1")

    @property
    def SERVICE_NAME(self):
        return self._setting('SERVICE_NAME', 'spid.test.it:8000')

    @property
    def SERVICE_DESCRIPTION(self):
        return self._setting('SERVICE_DESCRIPTION', 'something')

    @property
    def NAME_FORMAT(self):
        return self._setting('NAME_FORMAT', 'urn:oasis:names:tc:SAML:2.0:nameid-format:transient')

    @property
    def SP_PUBLIC_CERT(self):
        public_cert_path = self._setting('SP_PUBLIC_CERT', '')
        if public_cert_path == '':
            return None
        return open(public_cert_path).read()

    @property
    def SP_PUBLIC_CERT_PATH(self):
        return self._setting('SP_PUBLIC_CERT', '')

    @property
    def SP_PRIVATE_KEY(self):
        private_key_path = self._setting('SP_PRIVATE_KEY', '')
        if private_key_path == '':
            return None
        return open(private_key_path).read()

    @property
    def SP_PRIVATE_KEY_PATH(self):
        return self._setting('SP_PRIVATE_KEY', '')

    @property
    def SAML_METADATA_NAMESPACE(self):
        return self._setting('SAML_METADATA_NAMESPACE', 'urn:oasis:names:tc:SAML:2.0:metadata')

    @property
    def XML_SIGNATURE_NAMESPACE(self):
        return self._setting('XML_SIGNATURE_NAMESPACE', 'http://www.w3.org/2000/09/xmldsig#')

    @property
    def BINDING_REDIRECT_URN(self):
        return self._setting('BINDING_REDIRECT_URN', 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect')

    @property
    def LOGOUT_BINDING(self):
        return self._setting('LOGOUT_BINDING', 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST')

    @property
    def CONSUMER_BINDING(self):
        return self._setting('LOGOUT_BINDING', 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST')

    @property
    def SP_DEBUG(self):
        return self._setting('SP_DEBUG', True)

    @property
    def STRICT_CONFIG(self):
        return self._setting('STRICT_CONFIG', True)

    @property
    def EXTRA_SETTINGS(self):
        return self._setting('EXTRA_SETTINGS', {})

    @property
    def IS_BEHIND_PROXY(self):
        return self._setting('IS_BEHIND_PROXY', False)

    @property
    def config(self):
        config = {
            "strict": self.STRICT_CONFIG,
            "debug": self.SP_DEBUG,
            "sp": {
                "entityId": self.SP_ENTITY_ID,
                "assertionConsumerService": {
                    "url": self.SP_ASSERTION_CONSUMER_SERVICE,
                    "binding": self.CONSUMER_BINDING
                },
                "singleLogoutService": {
                    "url": self.SP_SINGLE_LOGOUT_SERVICE,
                    "binding": self.LOGOUT_BINDING
                },
                "attributeConsumingServiceIndex": self.SP_ATTRIBUTE_CONSUMING_SERVICE_INDEX,
                "NameIDFormat": self.NAME_FORMAT,
                "x509cert": self.SP_PUBLIC_CERT,
                "privateKey": self.SP_PRIVATE_KEY
            }
        }
        if self.EXTRA_SETTINGS:
            config.update(self.EXTRA_SETTINGS)
        return config

app_settings = AppSettings('SPID_')
