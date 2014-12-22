# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('varer', '0012_auto_20141222_0524'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salgsvarepris',
            name='kassenr',
        ),
        migrations.AddField(
            model_name='salgsvare',
            name='kassenr',
            field=models.PositiveSmallIntegerField(blank=True, help_text='Nr i varekatalog i kassa', null=True),
            preserve_default=True,
        ),
    ]
