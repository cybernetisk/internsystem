#!/bin/bash

# Fixtures must often be updated when changing a model.
# An convenient way to do this is:
#
# 1. Reload the fixtures by dropping the database and loading fixtures before model is updated
# 2. Move forward in Git history with new model and migrations
# 3. Run migrations
# 4. For each fixture that needs update, run something like this:
#    ./manage.py dumpdata --format yaml voucher >voucher/fixtures/voucher.yam
#    and for specific models:
#    ./manage.py dumpdata --format yaml core.user >core/fixtures/user.yaml

# load core first as most stuff have dependencies to it
./manage.py loaddata --app core user semester nfccard

./manage.py loaddata --app cal events
./manage.py loaddata --app members members
./manage.py loaddata --app varer varer
./manage.py loaddata --app voucher voucher
