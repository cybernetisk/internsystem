# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0002_auto_20151104_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voucheruselog',
            name='comment',
            field=models.CharField(null=True, max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='worklog',
            name='comment',
            field=models.CharField(null=True, max_length=100, blank=True),
        ),
    ]
