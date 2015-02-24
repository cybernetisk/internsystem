# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('varer', '0016_auto_20141227_0243'),
        ('z', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KassenavnMapping',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('nummer', models.PositiveSmallIntegerField(verbose_name='Nummer i kassa')),
                ('navn', models.CharField(max_length=30, verbose_name='Navn i kassa')),
                ('salgsvare', models.ForeignKey(to='varer.Salgsvare', related_name='kassenavn_mappinger')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
