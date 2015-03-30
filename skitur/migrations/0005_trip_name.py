# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skitur', '0004_participant_trip'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='name',
            field=models.CharField(max_length=128, default='', verbose_name='Trip name'),
            preserve_default=False,
        ),
    ]
