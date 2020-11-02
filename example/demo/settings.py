"""
Django settings for demo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import configparser

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, "settings.conf"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "0c7216)gs^ne$%3+je20zuo+g0&^6yb@e68qdr!^!r0hmb-6y+"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
SESSION_COOKIE_SAMESITE = "None"

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "spid",
)

MIDDLEWARE = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # 'django.middleware.csrf.CsrfViewMiddleware',
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

ROOT_URLCONF = "demo.urls"

STATIC_ROOT = os.path.join(BASE_DIR, "static/")

WSGI_APPLICATION = "demo.wsgi.application"

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/"

SAML_FOLDER = os.path.join(BASE_DIR, "saml")

SESSION_ENGINE = "django.contrib.sessions.backends.file"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": True,
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

SPID_IDENTITY_PROVIDERS = [
    ("arubaid", "Aruba ID"),
    ("infocertid", "Infocert ID"),
    ("namirialid", "Namirial ID"),
    ("posteid", "Poste ID"),
    ("sielteid", "Sielte ID"),
    ("spiditalia", "SPIDItalia Register.it"),
    ("timid", "Tim ID"),
]

SPID_IDENTITY_PROVIDERS_EID = [
    ("eid_test", "Nodo eIDAS Italian - QA"),
    ("eid_prod", "Nodo eIDAS Italian"),
]

if config.get("spid", "IDPS"):
    additional_idps = config.get("spid", "IDPS").split("|")
    for add_idp in additional_idps:
        idp = tuple(add_idp.split(";"))
        SPID_IDENTITY_PROVIDERS.append(idp)

SPID_IDP_NAME_QUALIFIERS = {
    "arubaid": "https://loginspid.aruba.it",
    "infocertid": "https://identity.infocert.it",
    "namirialid": "https://idp.namirialtsp.com/idp",
    "posteid": "https://posteid.poste.it",
    "sielteid": "https://identity.sieltecloud.it",
    "spiditalia": "https://spid.register.it",
    "timid": "https://login.id.tim.it/affwebservices/public/saml2sso",
    "eid_test": "https://sp-proxy.pre.eid.gov.it/spproxy/idpit",
    "eid_prod": "https://sp-proxy.eid.gov.it/spproxy/idpit",
}


if config.get("spid", "IDPS_NQ"):
    additional_idps = config.get("spid", "IDPS_NQ").split("|")
    for add_idp in additional_idps:
        idp = add_idp.split(";")
        SPID_IDP_NAME_QUALIFIERS[idp[0]] = idp[1]


SPID_IDP_METADATA_DIR = os.path.join(SAML_FOLDER, "spid-idp-metadata")
SPID_SP_PUBLIC_CERT = os.path.join(BASE_DIR, "saml/certs/sp.crt")
SPID_SP_PRIVATE_KEY = os.path.join(BASE_DIR, "saml/certs/sp.key")

SPID_SP_ENTITY_ID = config.get("spid", "SPID_SP_ENTITY_ID")
SPID_SP_ASSERTION_CONSUMER_SERVICE = config.get(
    "spid", "SPID_SP_ASSERTION_CONSUMER_SERVICE"
)
SPID_SP_SINGLE_LOGOUT_SERVICE = config.get("spid", "SPID_SP_SINGLE_LOGOUT_SERVICE")
# SPID_SP_ATTRIBUTE_CONSUMING_SERVICE_INDEX = "0"
SPID_SP_SERVICE_NAME = config.get("spid", "SPID_SP_SERVICE_NAME")

SPID_BAD_REQUEST_REDIRECT_PAGE = "index"

SPID_POST_LOGIN_URL = "index"
SPID_ERROR_PAGE_URL = "errors"

SPID_EXTRA_SETTINGS = {
    "security": {
        "nameIdEncrypted": False,
        "authnRequestsSigned": True,
        "logoutRequestSigned": True,
        "logoutResponseSigned": True,
        "signMetadata": False,
        "wantMessagesSigned": True,
        "wantAssertionsSigned": True,
        "wantNameId": True,
        "wantNameIdEncrypted": False,
        "wantAssertionsEncrypted": False,
        "signatureAlgorithm": "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256",
        "digestAlgorithm": "http://www.w3.org/2000/09/xmldsig-more#sha256",
        "requestedAuthnContext": ["https://www.spid.gov.it/SpidL2"],
    }
}
# Read X-Forwarded headers if present
SPID_IS_BEHIND_PROXY = False
SPID_BAD_REQUEST_REDIRECT_PAGE = "index"
SPID_ERROR_PAGE_URL = "errors"
