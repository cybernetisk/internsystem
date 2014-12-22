# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('varer', '0011_auto_20141222_0447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salgsvarepris',
            name='salgsvare',
            field=models.ForeignKey(to='varer.Salgsvare', related_name='priser'),
            preserve_default=True,
        ),
    ]
