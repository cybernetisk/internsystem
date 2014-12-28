# CYB-økonomi

CYB har i dag et Google Spreadsheet med alle varer vi har, hvor vi oppdaterer innkjøpspriser og salgspriser, og som gir oss en liten kalkyle over forventet resultat m.v.

Målet med dette prosjektet er å lage et bedre tilpasset system, slik at man kan ha historikk over priser, kanskje knytte det mot kassesystemet/Z-rapporter, mulighet for enklere vareopptelling med automatisk rapport til regnskap m.v.

## Oppsett
`npm` og `virtualenv` må være tilgjengelig på systemet.

Virtualenv:
* `$ virtualenv -p python3 env` (setter opp virtualenv for prosjektet, merk at vi bruker Python 3 og ikke Python 2)
* `$ source env/bin/activate` (aktiverer virtualenv i konsollen vår, må gjøres hver gang man går i ny konsoll for prosjektet)

Diverse pakker:
* `$ pip install -r requirements.txt` (installer Python-pakker fra `requirements.txt`)
* `$ npm install` (installerer nodejs-moduler som bower, gulp m.v., leser fra `package.json`)

Sett opp så bower og gulp kan kjøres enkelt:
* Rediger `env/bin/activate` og finn linjen med `PATH=`, endre til:
  * `PATH="$VIRTUAL_ENV/bin:$VIRTUAL_ENV/../node_modules/.bin:$PATH"`

Flere pakker:
* `$ bower install` (installerer bower-pakker som angular, jquery m.v., leser fra `bower.json`)

Sett opp database:
* Overstyr evt. sqlite med egen `DATABASES`-variabel i `settings_local.py`
* `$ ./manage.py migrate`

Lag static filer:
* `$ gulp`
* `$ ./manage.py collectstatic` (denne er kun nødvendig i produksjon)
