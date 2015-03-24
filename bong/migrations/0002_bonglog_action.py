# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bong', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bonglog',
            name='action',
            field=models.CharField(default='i', choices=[('i', 'issued'), ('s', 'spendt')], max_length=1),
            preserve_default=True,
        ),
    ]
