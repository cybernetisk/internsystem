# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('members', '0006_auto_20160219_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='comments',
            field=models.TextField(null=True, blank=True),
        ),
    ]
