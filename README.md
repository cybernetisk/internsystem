# CYBs internsystem
Dette prosjektet tilbyr en rekke tjenester til hjelp for Cybernetisk Selskab.

Tjenester prosjektet tilbyr i dag:
* Påloggingsløsning mot Universitet i Oslo med weblogin
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
* AngularJS i kombinasjon med ReactJS brukes i frontend
* Kommunikasjon mellom backend og frontend er REST-basert

Hvert "underprosjekt" har sin egen mappe, og "frontend-wrapper" er et eget prosjekt i mappen `siteroot` som er template og fellesting for frontend.

Et spesialprosjekt `core` har felles modeller som brukes av flere prosjekter.

Det brukes en del hjelpeprogrammer/verktøy, se resten av README for mer info.

## Sette opp systemet
For å forenkle oppsett er det laget et eget script som gjør alle nødvendige operasjoner. Man må først hente ned filene fra Git.

```bash
mkdir internsystem && cd internsystem # endre mappe om ønskelig
git clone git@github.com:cybrairai/okonomi.git .
./setup_dev.sh
```

Scriptet gjør følgende:
* Installerer systempakker (npm, virtualenv, python, m.v.) - derfor den spør om sudo passord
* Setter opp virtualenv ved hjelp av virtuelenvwrapper
* Installerer Python-pakker
* Installerer NodeJS-pakker
* Installerer Bower-pakker
* Setter opp lokale innstillinger for applikasjonen
* Migrerer databasen (standard vil bruke lokal sqqlite-database)
* Genererer frontend med `gulp`
* Starter utviklerserveren (Ctrl+C for å avslutte)

Man bør også lage en superbruker for å kunne logge inn:

```bash
./manage.py createsuperuser # husk at du må ha aktivert virtualenv!
```

Det kan også hentes inn demodata for at applikasjonen blir litt mer praktisk å teste lokalt:

```bash
./manage.py loaddata semester varer
```

### Bruke virtualenv
Pakken `virtualenvwrapper` installeres globalt, noe som gjør bruk av virtualenv veldig enkelt.
Som standard settes det opp et miljø som heter `internsystem`.

For å aktivere virtualenv og få tilgang til Python-pakkene for internsystemet skrives følgende:

```bash
workon internsystem
```

Det skal da stå `(internsystem)` i terminalen. Oppsettet vi bruker gjør også slik at node
sin `bin`-mappe havner i PATH.

### Avanserte innstillinger
For å f.eks. sette opp en annen database (f.eks. Postgres), må dette settes opp i `cyb_oko/settings_local.py`.

### Utvikling

#### Kjøre testserver
```bash
workon internsystem
gulp                  # frontend "build"
./manage.py migrate   # migrer database (trenger kun kjøres hvis det er gjort endringer i databaseskjemaer)
./manage.py runserver
#./manage.py runserver 0.0.0.0:8000 # example for allowing connections from others than local
```

#### Pålogging mot UiO-weblogin
Hvis man ikke vil knote med weblogin, kan man også logge inn i Django-admin (`/admin/`). Da blir man logget inn på resten av siden.

Alterantivt har vi også weblogin-adresse på `https://dev.internt.cyb.no`. Dette kan brukes på testserver ved å aktivere SSL samt sette dev.internt.cyb.no til 127.0.0.1 i hosts-filen. Filen `samlauth/settings.json` må i så fall endres.

#### Utviklingstips
Hver gang noe i frontend endres, må som regel `gulp` kjøres. For å forenkle dette kan man la `gulp watch` kjøre i bakgrunnen.

## Produksjonsserver
Vi har en [droplet hos Digital Ocean](https://confluence.cyb.no/display/AKTIV/Servere) som kjører systemet i produksjon. Den kjører `gunicorn` i kombinasjon med `nginx` for å kjøre Django-applikasjonen over port 80.

https://internt.cyb.no/

Prosjektet ligger i `~django/django_project`. For å komme inn på serveren brukes SSH-nøkler, så har du ikke tilgang ta kontakt med en som har. Dersom det logges inn med root, husk å bytte til django-brukeren: `su django`.

### Oppdatere produksjonsserver
Her er eksempel på prosess:
```bash
su django # om nødvendig
cd ~/django_project
./deploy-production.sh
```

Se `deploy-production.sh` for mer info. Gunicorn blir restartet når dette kjøres. Dette gjøres med `sudo` og `django`-brukeren har rettighet til å gjøre det uten passord iht. `/etc/sudoers`.
