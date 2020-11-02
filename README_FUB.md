# Introduzione

Questa libreria è un fork della libreria spid-django offerta da AgID per l'integrazione di SPID all'interno di progetti Django, ed è basata su un fork della libreria python3-saml anch'esso realizzato dalla Fondazione Ugo Bordoni e disponibile al seguente link: [https://github.com/fondazionebordoni/python3-saml](https://github.com/fondazionebordoni/python3-saml).
Il fork di questi due progetti è stato effettuato per adeguare la libreria python3-saml alle specifiche più recenti di SPID e per rendere l'integrazione del modulo spid-django più facile da integrare nei progetti Django, oltre a fornire il supporto ad eID che era assente nella versione originale.

# Installazione

Le due librerie sono presenti nel PyPI interno della FUB, pertanto possono essere installate con i comandi:

```
pip install --extra-index-url 'https://nexus.fub.it/repository/pypi-internal/simple' python3-saml
pip install --extra-index-url 'https://nexus.fub.it/repository/pypi-internal/simple' spid-django
```

Come spiegato in precedenza, questo fork di spid-django dipende dal fork di python3-saml, pertanto è necessario installare le due libreria nell'ordine mostrato affinché tutto funzioni correttamente.

# Configurazione del progetto Django

## Configurazione del file settings.py

Una volta installate le due libreria occorre modificare il file settings.py del progetto Django come segue:

- Aggiungere l'app "spid" ad INSTALLED_APPS:

```
INSTALLED_APPS = [
    # ...
    "spid",
]

```

- Aggiungere una variabile SPID_IDENTITY_PROVIDERS, che contiene una lista di tuple ciascuna delle quali rappresenta un IDP SPID. Ogni tupla contiene l'id interno all'app dell'IDP e il relativo nome da mostrare all'utente.

```
SPID_IDENTITY_PROVIDERS = [
    ("arubaid", "Aruba ID"),
    ("infocertid", "Infocert ID"),
    ("namirialid", "Namirial ID"),
    ("posteid", "Poste ID"),
    ("sielteid", "Sielte ID"),
    ("spiditalia", "SPIDItalia Register.it"),
    ("timid", "Tim ID"),
]
```

- Aggiungere una variabile SPID_IDENTITY_PROVIDERS_EID che contiene una lista di tuple ciascuna delle quali rappresenta un IDP eIDAS (di norma esiste un solo nodo eIDAS che opera da IDP per eID ma ne esistono due ambienti, rispettivamente di test e sviluppo). Ogni tupla contiene l'id interno all'app dell'IDP e il relativo nome da mostrare all'utente.

```
SPID_IDENTITY_PROVIDERS_EID = [
    ("eid_test", "Nodo eIDAS Italian - QA"),
    ("eid_prod", "Nodo eIDAS Italian"),
]
```

- Aggiungere una variabile SPID_IDP_NAME_QUALIFIERS contenente una dizionario in cui ogni coppia chiave-valore contiene l'id interno dell'IDP e una URL associata all'IDP, necessaria per lo scambio SAML tra SP ed IDP stesso (non ci sono particolari indicazioni su quale questa URL debba essere, pertanto finora abbiamo utilizzato il valore dell'entityID dell'IDP stesso).

```
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
```

- Aggiungere una variabile SAML_FOLDER contenente il path della directory che conterrà i metadata degli IDP, il metadata del Service Provider che si sta realizzando e le chiavi per firmare le richieste SAML in uscita (maggiori dettagli nelle sezioni successive).

```
SAML_FOLDER = os.path.join(BASE_DIR, "saml")
```

- Aggingere una variabile SPID_IDP_METADATA_DIR contenente il path della directory contenente i metadata degli IDP.

```
SPID_IDP_METADATA_DIR = os.path.join(SAML_FOLDER, "spid-idp-metadata")
```

- Aggiungere due variabili SPID_SP_PUBLIC_CERT e SPID_SP_PRIVATE_KEY contenenti il path rispettivamente del file con la chiave pubblica e del file con la chiave privata con cui vengono firmate le asserzioni SAML.

```
SPID_SP_PUBLIC_CERT = os.path.join(BASE_DIR, "saml/certs/sp.crt")
SPID_SP_PRIVATE_KEY = os.path.join(BASE_DIR, "saml/certs/sp.key")
```

- Aggiungere una variabile SPID_SP_ENTITY_ID contenente l'entityID del servizio che si sta realizzando.

```
SPID_SP_ENTITY_ID = "https://interazione.cvcn.it"
```

- Aggiungere una variabile SPID_SP_ASSERTION_CONSUMER_SERVICE contenente la URL a cui l'IDP deve rivolgersi, durante il processo di autenticazione, per il processamento della risposta SAML.

```
SPID_SP_ASSERTION_CONSUMER_SERVICE = "https://interazione.cvcn.it:2000/spid/attributes-consumer/"
```

- Aggiungere una variabile SPID_SP_SINGLE_LOGOUT_SERVICE contenente la URL a cui l'IDP deve rivolgersi al termine del processo di logout.

```
SPID_SP_SINGLE_LOGOUT_SERVICE = "http://interazione.cvcn.it/spid/sls-logout/"
```

- Aggiungere una variabile SPID_SP_SERVICE_NAME contenente il nome del servizio che si sta sviluppando.

```
SPID_SP_SERVICE_NAME = "interazione.cvcn.it"
```

- Aggiungere una variabile SPID_BAD_REQUEST_REDIRECT_PAGE contenente il nome della view a cui l'utente verrà reindirizzato in caso di errore durante il processo di login (o in caso di accesso scorretto alle URL delle view che implementano le varie operazioni di SPID).

```

SPID_BAD_REQUEST_REDIRECT_PAGE = "interazione_app:home"

```

- Aggiungere una variabile SPID_POST_LOGIN_URL contenente il nome della view a cui l'utente verrà reindirizzato al termine del login.

```

SPID_POST_LOGIN_URL = "interazione_app:spid_login"

```

- Aggiungere una variabile SPID_ERROR_PAGE_URL contenente il nome della view a cui l'utente verrà reindirizzato nel caso in cui venga rilevato un errore durante lo scambio SAML tra SP ed IDP.

```

SPID_ERROR_PAGE_URL = "interazione_app:spid_error"

```

- Se l'applicazione Django si trova dietro ad un frontend (e.g., Apache o Nginx), allora occorre aggiungere una variabile SPID_IS_BEHIND_PROXY con valore pari a True.

```

SPID_IS_BEHIND_PROXY = True

```

- Infine, occorre aggiungere una variabile SPID_EXTRA_SETTINGS che contiene un dizionario con alcuni parametri di configurazione da impostare in base alla propria implementazione di SPID.

```
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

```

### Nota

Una volta che l'utente ha effettuato l'accesso sull'IdentityProvider, abbiamo notato che, quando il browser riporta l'utente sul sito del Service provider, i cookie di sessione non vengono utilizzati, portando il processo di autenticazione ad un errore.
Per risolvere, l'unica soluzione che abbiamo trovato finora è quella di impostare il parametro SESSION_COOKIE_SAMESITE = "None" nel file settings.py del progetto Django.

## Configurazione urls.py

Nel file urls.py del progetto Django, aggiungere le url dell'app "spid".

```
urlpatterns = [
    # ...
    path("spid/", include("spid.urls")),
    # ...
]
```

# Creazione cartella indicata in 'SAML_FOLDER'

## Cartella con i metadata degli IDP

I metadata degli IDP vanno inseriti tutti dentro la cartella indicata in settings.py, indicando per ognuno di essi un nome con un formato specifico. Dato un IDP che è stato indicato come ("timid", "Tim ID") in SPID_IDENTITY_PROVIDERS, per esempio, il metadata di questo IDP va salvato in un file XML con nome "spid-idp-timid.xml", in modo da permettere alla libreria di recuperare automaticamente il metadata corretto durante il processo di login.

## Cartella con il metadata del SP

Il metadata del Service Provider a cui il progetto Django in questione fa riferimento va inserito in una cartella "spid-sp-metadata" e salvato come "metadata.xml".

## Cartella con le chiavi per firmare le richieste SAML

All'interno della cartella indicata in "SAML_FOLDER" occorre creare una cartella "certs" con le chiavi asimmetriche usare per firmare e verificare le richieste SAML inviate agli IDP (la chiave pubblica deve essere quella indicata nel metadata).

# Processamento della risposta

## Successo

In caso di successo, i dati dell'utente, specificati nell'attributeConsumer indicato nel metadata e di cui èstato indicato l'attributeConsumerIndex durante la richiesta di login, vengono inseriti all'interno della sessione sotto una chiave "samlUserdata", come indicato nell'esempio di sessione riportato di seguito.

```
dict_items([
    ('idp', 'samlcheck'),
    ('request_id', 'ONELOGIN_0f925f883478a7f226efa81ed7f57dc84cfe35d6'),
    ('request_instant', 1604306222.345485),
    ('attr_cons_index', '0'),
    ('samlUserdata', {
        'spidCode': ['AGID-001'],
        'name': ['SpidValidator'],
        'familyName': ['AgID'],
        'fiscalNumber': ['TINIT-GDASDV00A01H501J'],
        'email': ['spid.tech@agid.gov.it']
    }),
    ('samlNameId', '\n _617eed6b-179c-48f6-a931-a75b6858bf48\n '),
    ('samlSessionIndex', '_59e79c8a-2526-4bbb-bdfd-8c812e372a20'),
])
```

## Errore

In caso di errore, la libreria reindirizzerà l'utente alla URL indicata in settings.py indicando, nei query parameters, il codice dell'errore ed una sua descrizione, come indicato nell'esempio di seguito.

```
https://interazione.cvcn.it:2000/cvcn/interazione/error?errors=['invalid_response']&error_msg=IssueInstant is either too old or ahead of current date and time.
```

# Configurazione del frontend

Qualora il progetto Django sia esposto tramite un frontend (e.g., Apache o Nginx), è necessario aggiungere i seguenti header alle richieste HTTP verso l'applicazione per consentire il corretto funzionamento della libreria spid-django (che vi accederà tramite request.META): HTTP_X_FORWARDED_HOST, HTTP_X_FORWARDED_PROTO, HTTP_X_FORWARDED_PORT.
Ecco un esempio di configurazione di Apache.

```
RequestHeader set "X-Forwarded-Proto" "https"
RequestHeader set "X-Forwarded-Port" "2000"
```
