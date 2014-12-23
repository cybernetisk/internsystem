# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('varer', '0014_auto_20141223_2206'),
    ]

    operations = [
        migrations.AddField(
            model_name='råvarepris',
            name='aktiv',
            field=models.BooleanField(default=True, help_text='Hvorvidt dette er/har vært en reell råvarepris for oss'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='råvarepris',
            name='type',
            field=models.CharField(choices=[('FAKTURA', 'Fakturapris'), ('LISTE', 'Listepris'), ('UKJENT', 'Ukjent opprinnelse')], max_length=10, default='UKJENT'),
            preserve_default=True,
        ),
    ]
