# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skitur', '0005_trip_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cabin',
            options={'ordering': ['trip', 'name']},
        ),
        migrations.AlterModelOptions(
            name='participant',
            options={'ordering': ['trip', 'user']},
        ),
        migrations.AlterModelOptions(
            name='trip',
            options={'ordering': ['date', 'name']},
        ),
        migrations.AlterModelOptions(
            name='wish',
            options={'ordering': ['participant', 'wish'], 'verbose_name_plural': 'wishes'},
        ),
    ]
