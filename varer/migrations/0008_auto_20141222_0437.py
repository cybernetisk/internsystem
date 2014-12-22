# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('varer', '0007_råvarepris_pant'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='konto',
            options={'verbose_name_plural': 'kontoer', 'ordering': ['gruppe', 'innkjopskonto']},
        ),
        migrations.AlterModelOptions(
            name='leverandør',
            options={'verbose_name_plural': 'leverandorer', 'ordering': ['navn']},
        ),
        migrations.AlterModelOptions(
            name='varetellingvare',
            options={'ordering': ['varetelling', 'raavare']},
        ),
        migrations.RenameField(
            model_name='konto',
            old_name='innkjøpskonto',
            new_name='innkjopskonto',
        ),
        migrations.RenameField(
            model_name='råvare',
            old_name='innkjøpskonto',
            new_name='innkjopskonto',
        ),
        migrations.RenameField(
            model_name='råvarepris',
            old_name='leverandør',
            new_name='leverandor',
        ),
        migrations.RenameField(
            model_name='råvarepris',
            old_name='råvare',
            new_name='raavare',
        ),
        migrations.RenameField(
            model_name='salgsvare',
            old_name='råvarer',
            new_name='raavarer',
        ),
        migrations.RenameField(
            model_name='salgsvareråvare',
            old_name='råvare',
            new_name='raavare',
        ),
        migrations.RenameField(
            model_name='varetellingvare',
            old_name='råvare',
            new_name='raavare',
        ),
    ]
