# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('varer', '0002_auto_20141219_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leverandør',
            name='kommentar',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='råvare',
            name='kategori',
            field=models.CharField(null=True, max_length=50, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='råvarepris',
            name='bestillingskode',
            field=models.CharField(null=True, max_length=30, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='salgskalkyle',
            name='kommentar',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='salgskalkylevare',
            name='interngrad',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='salgsvare',
            name='kategori',
            field=models.CharField(null=True, max_length=50, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='salgsvarepris',
            name='kassenr',
            field=models.PositiveSmallIntegerField(null=True, help_text='Nr i varekatalog i kassa', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='salgsvarepris',
            name='pris_ekstern',
            field=models.PositiveSmallIntegerField(null=True, help_text='Eksternpris INK mva', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='salgsvarepris',
            name='pris_intern',
            field=models.PositiveSmallIntegerField(null=True, help_text='Internpris INK mva', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='varetelling',
            name='kommentar',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='varetellingvare',
            name='kommentar',
            field=models.CharField(null=True, max_length=150, blank=True),
            preserve_default=True,
        ),
    ]
