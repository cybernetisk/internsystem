# CYBs internsystem (backend)

| Master | Test |
| --- | --- |
| [![Build Status](https://travis-ci.org/cybernetisk/internsystem.svg?branch=master)](https://travis-ci.org/cybernetisk/internsystem) | [![Build Status](https://travis-ci.org/cybernetisk/internsystem.svg?branch=test)](https://travis-ci.org/cybernetisk/internsystem) |

Dette prosjektet tilbyr en rekke tjenester til hjelp for Cybernetisk Selskab.
I hovedsak tilbyr dette prosjektet kun et API, som brukes av blant annet
https://github.com/cybernetisk/internsystem-frontend.

Tjenester prosjektet tilbyr i dag:

* Påloggingsløsning mot Universitet i Oslo med Weblogin
* Vare- og priskatalog for Escape, med varetellingsfunksjon, marginoversikt m.v.
* Bongsystem for internbonger
* Medlemssystem for å registere medlemmer i foreningen.

Tjenester det jobbes med/planlegges:

* Kaffebonger
* Internliste (i stedet for tabeller i wikien/GARM-systemet)
* Z-rapport-statistikk
* Sentral brukerdatabase for CYB (kunne koble andre tjenester som wiki m.v. mot
  dette systemet, med pålogging videresendt mot UiO)

## Kort teknisk oversikt

* Django (Python 3) er backend for systemet
  * Django tilbyr også en innebygget admin-modul vi bruker en del.
* Django-applikasjonen pakkes i et Docker-image som vi kjører i miljøene
* Tilbyr et REST-API til bruk av andre tjenester
* I produksjon benyttes Postgres som database
* For frontend-detaljer, se https://github.com/cybernetisk/internsystem-frontend

Hvert "underprosjekt" har sin egen mappe. Et spesialprosjekt `core` har felles
modeller som brukes av flere prosjekter.

Det brukes en del hjelpeprogrammer/verktøy, se resten av README for mer info.

## Sette opp systemet lokalt

Applikasjonen kan kjøres lokalt på to måter:

1) Som et produksjonsbygg. For små endringer er dette praktisk da man
   kun er avhengig av å ha Docker og Docker Compose installert.
2) Fullt utviklingsmiljø. Dette krever at man har Python 3 installert,
   avhengigheter for SAML etc. Dette gir mulighet for integrasjon med
   IDE-er og mulighet til å kjøre lint-verktøy etc. lokalt.

Gamle oppsett som kan gi noe inspirasjon for pakker som må installeres:

* [setup_dev.sh](https://github.com/cybernetisk/internsystem/blob/45d7da9d5591a3e85ba12fdcdbba19ababfb22e5/scripts/setup_dev.sh)
* [setup_dev_mac.sh](https://github.com/cybernetisk/internsystem/blob/45d7da9d5591a3e85ba12fdcdbba19ababfb22e5/scripts/setup_dev_mac.sh)

### (Kun for Mac OS) Installer de følgende pakkene først
```
brew install coreutils Libxmlsec1 pkg-config
```

### Som et produksjonsbygg

```bash
make docker-init docker-run
```

### Fullt utviklingsmiljø

```bash
make init run
```

Det opprettes et virtual env i mappen `.venv` ved dette oppsettet, som kan
aktiveres slik før manuell kjøring av Python-kommandoer:

```bash
. .venv/bin/activate
```

Sjekk om ting er i tråd med kodestil:

```bash
make lint
```

Formatter kode automatisk:

```bash
make format
```

### Bruk av lokalt miljø

Gå til http://localhost:8000/api/

Du skal kunne logge inn med brukeren `cyb` og passord `cyb`. De andre brukerne
som opprettes har også passord `cyb`.

Konfigurasjon kan endres i `cyb_oko/settings_local.py`.

## Kjøre tester tilsvarende som i CI

```bash
TRAVIS_BUILD_NUMBER=dev ./scripts/travis-build-image.sh
./scripts/travis-test-app.sh
./scripts/travis-test-image.sh
```

## Pålogging mot UiO-weblogin

Hvis man ikke vil knote med weblogin, kan man også logge inn i Django-admin
(`/admin/`). Da blir man logget inn på resten av siden.

Alternativt har vi også weblogin-adresse på `https://dev.internt.cyb.no`.
Dette kan brukes på testserver ved å aktivere SSL samt sette dev.internt.cyb.no
til 127.0.0.1 i hosts-filen.

Se også [`scripts/connect_dev.sh`](scripts/connect_dev.sh) for å bruke den
reelle `dev.internt.cyb.no`-hosten og sende trafikk mot https videre over
tunnell til lokal devinstans. På `dev.internt.cyb.no` blir port 443 redirected
til `localhost:8000` uten TLS på samme server.

Som standard er ikke weblogin aktivert i internsystemet. Dette aktiveres ved
å aktivere SAML-støtte i den lokale innstillingsfilen (`settings_local.py`).
Adressene i `samlauth/dev/settings.json` må også oppdateres til å peke til
`dev.internt.cyb.no`.

## Autentisering mot API

Vi benytter [django-oauth-toolkit](https://github.com/evonove/django-oauth-toolkit)
som håndterer mye av autentiseringen ved bruk av API-et. Dette brukes imidlertid
ikke på frontend-versjonen av internsia, som bruker vanlige sessions.

Man er nødt til å opprette en såkalt applikasjon, f.eks. via
http://localhost:8000/o/applications/, hvor man så må bruke client_id for å
faktisk kunne bruke autentiseringstjenesten. En applikasjon vil f.eks. være
en mobilapp.

Nyttige ressurser:

* http://django-oauth-toolkit.readthedocs.org/en/latest/rest-framework/getting_started.html
* http://oauthlib.readthedocs.org/en/latest/oauth2/grants/grants.html
* http://requests-oauthlib.readthedocs.org/en/latest/oauth2_workflow.html
* https://tools.ietf.org/html/rfc6749
* `client_secret` skal aldri publiseres noe sted eller brukes på en webapp/mobilapp.

### Autentisering på eget utstyr, f.eks. kortlesere

TODO: Burde sannsynligvis heller bruke grant_type=authorization-code slik at man
kan logge inn på systembrukeren direkte på utstyret. Alternativt legge inn
authorization code etter man logger inn et annet sted/får generert authorization
code.

For f.eks. fysisk utstyr som bruker internsia som API benyttes grant typen
`password` (Resource Owner Password Credentials Grant), i kombinasjon med
brukere som opprettes spesifikt for utstyret. På denne måten får man autentisert
(siden man da har en client_id), og får korrekte rettigheter/tilganger
(siden man autentiserer en bestemt bruker).

Eksempel:

```bash
curl -X POST -d "grant_type=password&username=<username>&password=<pass>" \
  -u "<client_id>:<client_secret>" \
  https://dev.internt.cyb.no/o/token/
```

Man mottar da en access token og refresh token som tas vare på. I praksis kan
man generere dette en gang for deretter å f.eks. fjerne passordet på
systembrukeren. client_id, client_secret og access/refresh token legges med
andre ord inn i systemet som bruker API-et.

Dersom `client type` settes til `public` er ikke `client_secret` nødvendig.

## Produksjonsserver

Produksjon oppdateres automatisk ved push til `master`, samt test-instans
oppdateres ved push til `test`. Se `.travis.yml`.

Se https://github.com/cybernetisk/drift/tree/master/internsystem-backend
for detaljer om oppsett i produksjon.

https://in.cyb.no/

https://test.in.cyb.no/
