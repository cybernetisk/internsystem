#!/bin/bash

set -e

if [[ "$USER" != "django" ]]; then
  echo "Du må være logget inn som brukeren 'django' for å kjøre dette!"
  exit 1
fi

git pull origin master

cd "$(dirname "$0")"/..

# in case of critical error when running migration, backup database to more easily manually rollback
mkdir -p backups
backup_file="$(pwd)/backups/db.backup.$(date +%Y%m%d.%H%M%S).sql"
pg_dump django >"$backup_file"
echo "Database backup saved to $backup_file"

if [ -z "$VIRTUAL_ENV" ]; then
  source env/bin/activate
fi

pip install -r requirements.txt
pip install -r requirements_saml.txt
./manage.py migrate

# neste linje er kun nødvendig i produksjon pga. gunicorn og nginx
./manage.py collectstatic --noinput

# hvis neste ikke funker, sjekk /etc/sudoers
# bør inneholde: django ALL=(root) NOPASSWD:/usr/sbin/service gunicorn reload
# (såfremt brukeren heter `django`)
sudo /usr/sbin/service gunicorn reload
