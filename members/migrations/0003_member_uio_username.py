# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('members', '0002_auto_20160128_2253'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='uio_username',
            field=models.CharField(null=True, max_length=15),
        ),
    ]
