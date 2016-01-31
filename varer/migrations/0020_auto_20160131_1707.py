# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('varer', '0019_auto_20160131_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='varetellingvare',
            name='time_price',
            field=models.DateField(blank=True, help_text='Overstyring av tidspunkt varen skal prises', null=True),
        ),
    ]
