#!/bin/bash

VIRTUALENV=internsystem
VIRTUALENVACT=~/.virtualenvs/$VIRTUALENV/bin/activate

# Make the bash script abort on error
set -e

cd "$(dirname "$0")"/..

# Make sure we don't have any active environment
deativate 2>/dev/null || true

# Install needed packages for the system
# (the second line is for packages used by python3-saml:)
if command -v brew > /dev/null; then
	brew install python3
else
	echo "Sure you are on a mac with homebrew?"
fi

if command -v pip3 > /dev/null; then
	echo "pip be good :D Installing virtualenv!"
	sudo pip3 install virtualenv virtualenvwrapper
else
	echo "Ensuring pip for you :)"
	python3 -m ensurepip
	echo "...and installing virtualenv"
	sudo pip3 install virtualenv virtualenvwrapper
fi

# Set up virtualenv for Python
# This will let us install Python-packages for this project only
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv -p /usr/local/bin/python3 $VIRTUALENV || true

if [ ! -f "$VIRTUALENVACT" ]; then
    echo "Setup of virtualenv failed, cannot find installation"
    exit 1
fi

# Set up settings file
EXAMPLEFILE=cyb_oko/settings_local_example.py
REALFILE=cyb_oko/settings_local.py
if [ ! -f "$REALFILE" ]; then
    RANDKEY=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
    cp "$EXAMPLEFILE" "$REALFILE"
    sed -i "s~^SECRET_KEY.*~SECRET_KEY = '$RANDKEY'~" "$REALFILE"
fi

# Activate the virtual environment
workon $VIRTUALENV

# Install Python dependencies from pip
pip install -r requirements.txt

# Migrate Django's database
./manage.py migrate

# Load fixtures
scripts/load_fixtures.sh

# Run development server
./manage.py runserver
