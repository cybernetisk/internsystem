# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('varer', '0006_auto_20141220_0452'),
    ]

    operations = [
        migrations.AddField(
            model_name='råvarepris',
            name='pant',
            field=models.FloatField(help_text='Pant per stk', default=0),
            preserve_default=True,
        ),
    ]
