# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('varer', '0010_raavare_lenket_salgsvare'),
    ]

    operations = [
        migrations.AlterField(
            model_name='råvare',
            name='lenket_salgsvare',
            field=models.ForeignKey(blank=True, null=True, to='varer.Salgsvare', related_name='lenkede_raavarer', on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
