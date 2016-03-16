# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('intern', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intern',
            name='comments',
            field=models.CharField(max_length=300, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='interngroup',
            name='description',
            field=models.CharField(max_length=300, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='internrole',
            name='description',
            field=models.CharField(max_length=300, blank=True, null=True),
        ),
    ]
