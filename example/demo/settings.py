"""
Django settings for demo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "0c7216)gs^ne$%3+je20zuo+g0&^6yb@e68qdr!^!r0hmb-6y+"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "*",
]

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
    },
]

SPID_IDENTITY_PROVIDERS = [
    ('arubaid', 'Aruba ID'),
    ('infocertid', 'Infocert ID'),
    ('namirialid', 'Namirial ID'),
    ('posteid', 'Poste ID'),
    ('sielteid', 'Sielte ID'),
    ('spiditalia', 'SPIDItalia Register.it'),
    ('timid', 'Tim ID')
]
SPID_IDP_METADATA_DIR = os.path.join(SAML_FOLDER, 'spid-idp-metadata')
SPID_SP_ENTITY_ID = "https://spid.test.it"
SPID_SP_ASSERTION_CONSUMER_SERVICE = "http://spid.test.it:8000/spid/attributes-consumer/"
SPID_SP_SINGLE_LOGOUT_SERVICE = "http://spid.test.it:8000/spid/sls-logout/"
SPID_SP_SERVICE_NAME = "spid.test.it:8000"
SPID_SP_PUBLIC_CERT = os.path.join(BASE_DIR, 'saml/certs/sp.crt')
SPID_SP_PRIVATE_KEY = os.path.join(BASE_DIR, 'saml/certs/sp.key')
SPID_EXTRA_SETTINGS = \
    {
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
            "requestedAuthnContext": ["https://www.spid.gov.it/SpidL2"]
        }
    }
# Read X-Forwarded headers if present
SPID_IS_BEHIND_PROXY = False
SPID_BAD_REQUEST_REDIRECT_PAGE = 'index'
SPID_ERROR_PAGE_URL = 'errors'