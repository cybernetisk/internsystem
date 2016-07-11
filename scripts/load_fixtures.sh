#!/bin/bash

# load core first as most stuff have dependencies to it
./manage.py loaddata --app core user semester nfccard

./manage.py loaddata --app cal events
./manage.py loaddata --app members members
./manage.py loaddata --app varer varer
./manage.py loaddata --app voucher voucher
