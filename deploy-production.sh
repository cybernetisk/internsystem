#!/bin/bash

# Deploy for produksjonsserver
# (brukes kun på produksjon)

if [[ "$USER" != "django" ]]; then
	echo "Du må være logget inn som brukeren 'django' for å kjøre dette!"
	exit 1
fi

if [ -z "$VIRTUAL_ENV" ]; then
	source env/bin/activate
fi

git pull
gulp build

# neste linje er kun nødvendig i produksjon pga. gunicorn og nginx
./manage.py collectstatic --noinput

# hvis neste ikke funker, sjekk /etc/sudoers
# bør inneholde: django ALL=(root) NOPASSWD:/usr/sbin/service gunicorn reload
# (såfremt brukeren heter `django`)
sudo /usr/sbin/service gunicorn reload

