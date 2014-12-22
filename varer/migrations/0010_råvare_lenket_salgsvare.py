# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('varer', '0009_auto_20141222_0437'),
    ]

    operations = [
        migrations.AddField(
            model_name='råvare',
            name='lenket_salgsvare',
            field=models.ForeignKey(blank=True, null=True, to='varer.Råvarepris', related_name='lenkede_raavarer'),
            preserve_default=True,
        ),
    ]
