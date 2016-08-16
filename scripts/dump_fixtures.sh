#!/bin/bash

# This script should normally only be ran after loading a clean database with fixtures
# to update the format of fixtures, e.g. in database migrations.

# An example of how to do this:
# 1. Reload the fixtures by dropping the database and loading fixtures before model is updated
# 2. Move forward in Git history with new model and migrations
# 3. Run migrations
# 4. Run this script and investigate the changes that is applied to the files before committing

# using json-format instead of yaml on normal fixtures due to yaml not handling timezone-aware dates
# see https://code.djangoproject.com/ticket/18867#comment:5

./manage.py dumpdata --format json core.user >core/fixtures/user.json
./manage.py dumpdata --format json core.semester >core/fixtures/semester.json
./manage.py dumpdata --format json core.nfccard >core/fixtures/nfccard.json

./manage.py dumpdata --format json cal.event >cal/fixtures/event.json

./manage.py dumpdata --format json members >members/fixtures/members.json

./manage.py dumpdata --format json varer >varer/fixtures/varer.json

./manage.py dumpdata --format json voucher >voucher/fixtures/voucher.json

./manage.py dumpdata --format json intern.accesslevel >intern/fixtures/accesslevels.json
./manage.py dumpdata --format json intern.role >intern/fixtures/roles.json
./manage.py dumpdata --format json intern.interngroup >intern/fixtures/groups.json
./manage.py dumpdata --format json intern.intern >intern/fixtures/interns.json
./manage.py dumpdata --format json intern.internlogentry >intern/fixtures/internlogs.json
./manage.py dumpdata --format json intern.internrole >intern/fixtures/internroles.json

# reformat the json so its fields are ordered
for file in */fixtures/*.json; do
    OUT=$(python -m json.tool "$file")
    if [ "$(cat "$file")" != "$OUT" ]; then
        echo "$OUT" >"$file"
    fi
done
