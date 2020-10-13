# django-spid-demo

Demo of a Django app using SPID authentication. This is just to show how it works.

# Requirements

**_IMPORTANT_**

In order to work with SPID, a modified version of python3-saml must be used, find it here:

https://github.com/fondazionebordoni/python3-saml/tree/spid-adaptation

You must also install the current projects, e.g. using

pip install ../

after this, you can now install the requirements as usual.

# Identity Provider

You need to have access to an Identity Provider (IdP), for testing purposes you can use

https://github.com/italia/spid-testenv2

Save the metadata of the IdP in

- `../spid/spid-idp-metadata`
- `../spid/app_settings.py`
- `../spid/static/spid/spid-sp-access-button.html`

# Service Provider

Verify and adjust the settings in `./saml` and `demo/settings.py`, and start the application with

`python manage.py runserver`

You can get the SP metadata from http://localhost:8000/spid/metadata

Install this metadata in the IdP. Now it should be possible to authenticate.
