# CYB-økonomi
Tidligere har vi benyttet diverse regneark for å holde oversikt over prisfastsetting m.v. I 2014 ble dette utvidet til å være en komplett varekatalog over alle varene vi har, deres innkjøpspris og salgspris m.v.

Målet med dette prosjektet er å lage et bedre tilpasset system, slik at man kan ha historikk over priser, kanskje knytte det mot kassesystemet/Z-rapporter, mulighet for enklere vareopptelling med rapport til regnskap m.v.

## Kort teknisk oversikt
Django (Python 3) er backend for systemet, mens AngularJS i kombinasjon med ReactJS brukes i frontend. Kommunikasjon mellom backend og frontend er REST-basert. Django tilbyr også en innebygget admin-modul vi bruker en del.

Hvert "underprosjekt" har sin egen mappe, og "frontend-wrapper" er et eget prosjekt i mappen `siteroot` som er template og fellesting for frontend.

Det brukes en del hjelpeprogrammer/verktøy, se resten av README for mer info.

## Sette opp systemet

### Forutsetninger
`npm` og `virtualenv` må være tilgjengelig på systemet, i tillegg til Python 3. (F.eks. `sudo apt-get install npm virtualenv python3`)

### Grunnoppsett
Sørg for at du er i mappen du ønsker å ha prosjektet, bør være tom!
```bash
git clone git@github.com:cybrairai/okonomi.git .
virtualenv -p python3 env        # virtualenv sørger for at Python-pakker er lokale for prosjektet
source env/bin/activate          # for å "bruke" virtualenv må dette skrives
pip install -r requirements.txt  # installerer Python-pakker
npm install                      # installer NodeJS-moduler (hjelpeverktøy) fra package.json
```

For å kunne kjøre NodeJS-modulene, åpne `env/bin/activiate` og rediger linjen med `PATH=` til:
`PATH="$VIRTUAL_ENV/bin:$VIRTUAL_ENV/../node_modules/.bin:$PATH"`

```bash
bower install   # installerer angular, jquery m.v.
```

Vi må sette opp litt lokal konfigurasjon før vi fortsetter. Kopier følgende til `cyb_oko/settings_local.py`
og rediger innholdet. Det som settes opp her overstyrer `cyb_oko/settings.py`.

```python
# this should be unique
SECRET_KEY = 'edit-me'

# see https://docs.djangoproject.com/en/1.7/ref/settings/#std:setting-DEBUG
DEBUG = True

# see https://docs.djangoproject.com/en/1.7/ref/settings/#std:setting-ALLOWED_HOSTS
#ALLOWED_HOSTS = [
#    'something',
#]

# if collectstatic is used, set up this
#STATIC_ROOT = "/home/django/django_project/env/static/"

# example for postgres configuration
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'django',
#        'USER': 'django',
#        'PASSWORD': 'edit-me',
#        'HOST': '127.0.0.1',
#        'PORT': '5432',
#    }
#}

# to log the queries in console, uncomment this
#LOGGING = {
#    'version': 1,
#    'handlers': {
#        'console': {
#            'level': 'DEBUG',
#            'class': 'logging.StreamHandler'
#        }
#    },
#    'loggers': {
#        'cyb_oko.querydebug': {
#            'handlers': ['console'],
#            'level': 'DEBUG'
#        },
#        'django.db.backends': {
#            'level': 'DEBUG',
#            'handlers': ['console']
#        }
#    }
#}
```

Nå skal vi sette opp databasen. Django kjører alle databasemigrasjoner for å få til dette.
Som standard bruker Django en SQLite-database som lagres sammen med prosjektet.
For å sette opp en annen database (f.eks. Postgres), må dette settes opp i `cyb_oko/settings_local.py`.

```bash
./manage.py migrate # initialiserer databasen
```

### Kjøre testserver
```bash
gulp                  # frontend "build"
./manage.py migrate   # migrer database (trenger kun kjøres hvis det er gjort endringer i databaseskjemaer)
./manage.py runserver
```

### Utviklingstips
Hver gang noe i frontend endres, må som regel `gulp` kjøres. For å forenkle dette kan man la `gulp watch` kjøre i bakgrunnen.

## Produksjonsserver
Vi har en droplet hos Digital Ocean som kjører systemet i produksjon. Den kjører `gunicorn` i kombinasjon med `nginx` for å kjøre Django-applikasjonen over port 80.

http://cyb.hsw.no/

Prosjektet ligger i `~django/django_project`. For å komme inn på serveren brukes SSH-nøkler, så har du ikke tilgang ta kontakt med en som har. Dersom det logges inn med root, husk å bytte til django-brukeren: `su django`.

### Oppdatere produksjonsserver
Her er eksempel på prosess:
```bash
su django # om nødvendig
cd ~/django_project
./deploy-production.sh
```

Se `deploy-production.sh` for mer info. Gunicorn blir restartet når dette kjøres. Dette gjøres med `sudo` og `django`-brukeren har rettighet til å gjøre det uten passord iht. `/etc/sudoers`.
