# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('varer', '0005_auto_20141220_0405'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='konto',
            options={'verbose_name_plural': 'kontoer', 'ordering': ['gruppe', 'innkjøpskonto']},
        ),
        migrations.RenameField(
            model_name='konto',
            old_name='kortnavn',
            new_name='gruppe',
        ),
    ]
