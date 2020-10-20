# django-spid-demo

Demo of a Django app using SPID authentication. This is just to show how it works.

# Requirements

**_IMPORTANT_**

In order to work with SPID, a modified version of python3-saml must be used, find it here:

https://github.com/fondazionebordoni/python3-saml/tree/spid-adaptation

You must also install the current project, e.g. using

pip install ../

after this, you can now install the requirements as usual.

# Identity Provider

You need to have access to an Identity Provider (IdP), for testing purposes you can use

https://github.com/italia/spid-testenv2

Save the metadata of the IdP in

- `../spid/spid-idp-metadata`
- `../spid/app_settings.py`

# Service Provider

- create certificates that should be placed in saml/certs (or use the ones provided for testing)
- create the metadata.xml file or modify the one provided, especially you need to modify the entityID and service URL and install it in the IdP server
- the AttributeConsumingService should be used in the SPID button in order to specify the requested attributes

Verify and adjust the settings and files in `demo/settings.py`:

- if the application is running behind a proxy, e.g. nginx, you should set SPID_IS_BEHIND_PROXY to True, and make sure that nginx is setting the X-Forwarded-Host, X-Forwarded-Port and X-Forwarded-Proto headers
- SPID_SP_ENTITY_ID, SPID_SP_ASSERTION_CONSUMER_SERVICE and SPID_SP_SINGLE_LOGOUT_SERVICE should correspond to the metadata.xml

run with

`python manage.py runserver`

# Running with docker-compose

Use a certificate created by you or generate a self signed certificate with

```
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout conf/conf.d/nginx-selfsigned.key -out conf/conf.d/nginx-selfsigned.crt
```

Run `docker-compose up`.
