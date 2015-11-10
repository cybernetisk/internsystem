# CYBs internsystem (backend)
Dette prosjektet tilbyr en rekke tjenester til hjelp for Cybernetisk Selskab. I hovedsak tilbyr dette prosjektet kun et API, som brukes av blant annet https://github.com/cybrairai/internsystem-frontend.

Tjenester prosjektet tilbyr i dag:
* Påloggingsløsning mot Universitet i Oslo med Weblogin
* Vare- og priskatalog for Escape, med varetellingsfunksjon, marginoversikt m.v.

Tjenester det jobbes med/planlegges:
* Ta over for [eksisterende medlemssystem](https://github.com/vegarang/medlemssystem_django)
* Elektronisk bongsystem (i stedet for Google Spreadsheets)
* Internliste (i stedet for tabeller i wikien)
* Z-rapport-statistikk
* Sentral brukerdatabase for CYB (kunne koble andre tjenester som wiki m.v. mot dette systemet, med pålogging videresendt mot UiO)

## Kort teknisk oversikt
* Django (Python 3) er backend for systemet
** Django tilbyr også en innebygget admin-modul vi bruker en del.
* Tilbyr et REST-API til bruk av andre tjenester
* I produksjon benyttes Postgres som database
* For frontend-detaljer, se https://github.com/cybrairai/internsystem-frontend

Hvert "underprosjekt" har sin egen mappe. Et spesialprosjekt `core` har felles modeller som brukes av flere prosjekter.

Det brukes en del hjelpeprogrammer/verktøy, se resten av README for mer info.

## Sette opp systemet
For å forenkle oppsett er det laget et eget script som gjør alle nødvendige operasjoner. Man må først hente ned filene fra Git.

```bash
mkdir internsystem && cd internsystem # endre mappe om ønskelig
git clone git@github.com:cybrairai/internsystem.git .
./scripts/setup_dev.sh
```

Scriptet gjør følgende:
* Installerer systempakker (virtualenv, python, m.v.) - derfor den spør om sudo passord
* Setter opp virtualenv ved hjelp av virtuelenvwrapper
* Installerer Python-pakker
* Setter opp lokale innstillinger for applikasjonen
* Migrerer databasen (standard vil bruke lokal sqqlite-database)
* Starter utviklerserveren for backend (Ctrl+C for å avslutte)

Man bør også lage en superbruker for å kunne logge inn:

```bash
./manage.py createsuperuser # husk at du må ha aktivert virtualenv!
```

Det kan også hentes inn demodata for at applikasjonen blir litt mer praktisk å teste lokalt:

```bash
./manage.py loaddata semester varer events
```

### Bruke virtualenv
Pakken `virtualenvwrapper` installeres globalt, noe som gjør bruk av virtualenv veldig enkelt.
Som standard settes det opp et miljø som heter `internsystem`.

For å aktivere virtualenv og få tilgang til Python-pakkene for internsystemet skrives følgende:

```bash
workon internsystem
```

Det skal da stå `(internsystem)` i terminalen.

### Avanserte innstillinger
For å f.eks. sette opp en annen database (f.eks. Postgres), må dette settes opp i `cyb_oko/settings_local.py`.

### Utvikling

#### Kjøre testserver
```bash
workon internsystem
./manage.py migrate   # migrer database (trenger kun kjøres hvis det er gjort endringer i databaseskjemaer)
./manage.py runserver
#./manage.py runserver 0.0.0.0:8000 # example for allowing connections from others than local
```

#### Pålogging mot UiO-weblogin
Hvis man ikke vil knote med weblogin, kan man også logge inn i Django-admin (`/admin/`). Da blir man logget inn på resten av siden.

Alternativt har vi også weblogin-adresse på `https://dev.internt.cyb.no`. Dette kan brukes på testserver ved å aktivere
SSL samt sette dev.internt.cyb.no til 127.0.0.1 i hosts-filen. Filen `samlauth/settings.json` må i så fall endres, slik
at ting peker til `dev.internt.cyb.no`.

Se også [`scripts/connect_dev.sh`](scripts/connect_dev.sh) for å bruke den reelle `dev.internt.cyb.no`-hosten og
sende trafikk mot https videre over tunnell til lokal devinstans. På `dev.internt.cyb.no` blir port 443 redirected
til `localhost:8000` uten TLS på samme server.

Som standard er ikke weblogin aktivert i internsystemet. Dette aktiveres ved å kjøre `scripts/setup_saml.sh`-scriptet og aktivere SAML-støtte i den lokale innstilingsfilen (`settings_local.py`).

## Autentisering mot API
Vi benytter [django-oauth-toolkit](https://github.com/evonove/django-oauth-toolkit) som håndterer mye av autentiseringen
ved bruk av API-et. Dette brukes imidlertid ikke på frontend-versjonen av internsia, som bruker vanlige sessions.

Man er nødt til å opprette en såkalt applikasjon, f.eks. via http://localhost:8000/o/applications/, hvor man så
må bruke client_id for å faktisk kunne bruke autentiseringstjenesten. En applikasjon vil f.eks. være en mobilapp.

Nyttige ressurser:
* http://django-oauth-toolkit.readthedocs.org/en/latest/rest-framework/getting_started.html
* http://oauthlib.readthedocs.org/en/latest/oauth2/grants/grants.html
* http://requests-oauthlib.readthedocs.org/en/latest/oauth2_workflow.html
* `client_secret` skal aldri publiseres noe sted eller brukes på en webapp/mobilapp.

## Produksjonsserver
Vi har en [droplet hos Digital Ocean](https://confluence.cyb.no/display/AKTIV/Servere) som kjører systemet i produksjon. Den kjører `gunicorn` i kombinasjon med `nginx` for å kjøre Django-applikasjonen over port 80.

https://internt.cyb.no/

Prosjektet ligger i `~django/django_project`. For å komme inn på serveren brukes SSH-nøkler, så har du ikke tilgang ta kontakt med en som har. Dersom det logges inn med root, husk å bytte til django-brukeren: `su django`.

### Oppdatere produksjonsserver
Dette skjer automatisk ved push til master. Se `.travis.yml` og `scripts/deploy.sh` for detaljer.

## Dependencies on Mac OS X

```bash
# Install libxml and libxmlsec
brew install libxml2 libxmlsec1
```

Fix virtualenv (somehow) …

```bash
# Set include path to include libxmlsec
export C_INCLUDE_PATH=/usr/local/Cellar/libxmlsec1/1.2.20/include/xmlsec1/

# Install manual dependency not in pip
pip install git+https://github.com/bgaifullin/python3-saml.git

# Install Python dependencies from pip
pip install -r requirements.txt
```
Do other stuff …
