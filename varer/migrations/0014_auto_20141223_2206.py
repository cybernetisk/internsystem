# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('varer', '0013_auto_20141222_0558'),
    ]

    operations = [
        migrations.AddField(
            model_name='råvare',
            name='antall',
            field=models.FloatField(help_text='Antall salgsbare enheter 1 stk gir', default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='råvarepris',
            name='leverandor',
            field=models.ForeignKey(to='varer.Leverandør', related_name='priser', blank=True, null=True),
            preserve_default=True,
        ),
    ]
