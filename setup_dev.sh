#!/bin/bash

VIRTUALENV=internsystem
VIRTUALENVACT=~/.virtualenvs/$VIRTUALENV/bin/activate
NODEBIN=`pwd`/node_modules/.bin

# Make the bash script abort on error
set -e

# Make sure we don't have any active environment
deativate 2>/dev/null || true

# Install needed packages for the system
# (the second line is for packages used by python3-saml:)
sudo apt-get install npm virtualenv virtualenvwrapper python3 \
             python3-dev libxslt1-dev libxml2-dev libxmlsec1-dev pkg-config

# Set up virtualenv for Python
# This will let us install Python-packages for this project only
source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
mkvirtualenv -p /usr/bin/python3 $VIRTUALENV || true

if [ ! -f "$VIRTUALENVACT" ]; then
    echo "Setup of virtualenv failed, cannot find installation"
    exit 1
fi

# Add node's bin folder to virtualenv path
if ! grep -q "$NODEBIN" "$VIRTUALENVACT"; then
    sed -i "s~^\(export PATH\)\$~PATH=\"$NODEBIN:\$PATH\"\n\1~" "$VIRTUALENVACT"
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

# Install manual dependency not in pip
pip install git+https://github.com/bgaifullin/python3-saml.git

# Install Python dependencies from pip
pip install -r requirements.txt

# Install nodejs modules (reads from package.json)
npm install

# Install bower components (reads from bower.json)
bower install

# Migrate Django's database
./manage.py migrate

# Generate frontend files
gulp

# Run development server
./manage.py runserver

