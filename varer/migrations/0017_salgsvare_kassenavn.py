# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('varer', '0016_auto_20141227_0243'),
    ]

    operations = [
        migrations.AddField(
            model_name='salgsvare',
            name='kassenavn',
            field=models.CharField(max_length=15, help_text='Navn i varekatalog i kassa', blank=True, null=True),
            preserve_default=True,
        ),
    ]
