# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('z', '0002_kassenavnmapping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kassenavnmapping',
            name='navn',
            field=models.CharField(verbose_name='Navn i kassa', max_length=15),
            preserve_default=True,
        ),
    ]
