# django-spid-demo

Demo of a SPID authentication for Django,
based on [python3-saml](https://github.com/onelogin/python3-saml).

# Introduction

This is a django project with one demo app, that shows how to use
Single Sign On authentication through a SPID Identity Provider (SAML).

Technical documentation on SPID and SAML is available at:
https://github.com/italia/spid-docs ~~and
https://github.com/umbros/spid-docs/blob/master/pages/documentazione-e-utilita.md~~

# Installation

## General overview

In order to work with SPID, a modified version of python3-saml has to be used, you can find it here:

https://github.com/fondazionebordoni/python3-saml/tree/spid-adaptation

- Install django-spid and the modified python3-saml in your virtualenv and add django-spid to the project INSTALLED_APPS.
- Add spid urls to your project url patterns
- Generate X.509 certificates and store them somewhere
- Register your SP with the IdP.
- Start the app server

## Local development details

A **test identity provider** can be installed on your development environment
(your laptop?), following instructions at:

https://github.com/italia/spid-testenv2

Here follows more detailed steps with some suggestions:

- choose a domain for your Service Provider (i.e. spid.yourdomain.it)

- generate self-signed certificates for your SP (you can do that here:
  https://developers.onelogin.com/saml/online-tools/x509-certs/obtain-self-signed-certs)

- put the content of the generated certificates under `saml/certs/`
  (name them: sp.crt, sp.key and sp.csr; CSR is not useed here, I think)

- modify your /etc/hosts file, to redirect both
  `spid-testenv-identityserver` and `spid.yourdomain.it` to your `localhost`

  ```
  echo "127.0.0.1 spid-testenv-identityserver" | sudo tee -a /etc/hosts
  ```

- add your metadata to the IdP test server

- get the IdP metadata from the IdP test server and copy into spid-idp-metadata, and add the server in app_settings.py

# Useful debugging tools

- browser extensions to track SAML requests and response
  (they exist both for Chrome and Firefox)
- the "tools" tab within the `carbon` admin interface of the IdP
  (9443, admin/admin), that allows the verification of the requests.

# Execution

When the server is running, the home page shows a login button that
starts the SSO workflow.

Pressing the login button, a request is packed and sent to the IdP.

The IdP responds by redirecting you to its own login page.

You insert your credentials (you will need to create a user first)

The IdP redirects you to your SP, and visiting the page attrs you can se which
attributes have been loaded.

# TODOs

- Automatically load IdP data from metadata, to avoid the list of IdPs in app_settings.py

- IdP metadata should be in the Django app, not in the library

- improve session management (where to store attributes)

- tests

- improve doc

Copyright (c) 2017, the respective contributors, as shown by the AUTHORS file.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
