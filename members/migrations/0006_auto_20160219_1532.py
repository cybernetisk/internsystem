# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('members', '0005_auto_20160219_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='honorary',
            field=models.BooleanField(default=False, help_text='Honorary member'),
        ),
        migrations.AlterField(
            model_name='member',
            name='lifetime',
            field=models.BooleanField(default=False, help_text='Lifetime member'),
        ),
    ]
