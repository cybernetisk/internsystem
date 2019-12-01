# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('varer', '0008_auto_20141222_0437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='råvare',
            name='innkjopskonto',
            field=models.ForeignKey(to='varer.Konto', related_name='raavarer', on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
