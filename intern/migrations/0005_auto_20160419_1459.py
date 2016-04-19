# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('intern', '0004_auto_20160316_0045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='internaccesscard',
            name='card',
        ),
        migrations.RemoveField(
            model_name='internaccesscard',
            name='intern',
        ),
        migrations.DeleteModel(
            name='InternAccessCard',
        ),
    ]
