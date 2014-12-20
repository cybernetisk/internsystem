# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('varer', '0004_auto_20141220_0347'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='konto',
            options={'verbose_name_plural': 'kontoer', 'ordering': ['innkjøpskonto']},
        ),
        migrations.AddField(
            model_name='konto',
            name='kommentar',
            field=models.TextField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
