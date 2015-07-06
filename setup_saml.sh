#!/bin/bash

# the project must be up and running before using this script!

# Make the bash script abort on error
set -e

if ! [ -v VIRTUAL_ENV ]; then
    echo "A virtual environment must be activated before running this script"
    echo "Type \`workon\` to see possible environments"
    exit 1
fi

sudo apt-get install python3-dev libxslt1-dev libxml2-dev libxmlsec1-dev pkg-config

# Install manual dependency not in pip
pip install git+https://github.com/bgaifullin/python3-saml.git

# Install Python dependencies from pip
pip install -r requirements_saml.txt

echo "SAML-support is set up. Activate by changing local configuration."

