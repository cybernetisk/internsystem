# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0003_auto_20160124_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worklog',
            name='hours',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
        migrations.AlterField(
            model_name='worklog',
            name='vouchers',
            field=models.DecimalField(decimal_places=2, blank=True, max_digits=8),
        ),
    ]
