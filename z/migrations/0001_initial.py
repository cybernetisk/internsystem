# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('varer', '0016_auto_20141227_0243'),
    ]

    operations = [
        migrations.CreateModel(
            name='Kvittering',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nummer', models.PositiveIntegerField(verbose_name='Kvitteringsnummer')),
                ('tidspunkt', models.DateTimeField(verbose_name='Tidspunkt')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Varetransaksjon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('antall', models.IntegerField(verbose_name='Antall varer')),
                ('tidspunkt', models.DateTimeField(verbose_name='Tidspunkt for transaksjon')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Kassetransaksjon',
            fields=[
                ('varetransaksjon_ptr', models.OneToOneField(to='z.Varetransaksjon', primary_key=True, auto_created=True, serialize=False, parent_link=True)),
                ('kvittering', models.ForeignKey(to='z.Kvittering', related_name='transaksjoner')),
            ],
            options={
            },
            bases=('z.varetransaksjon',),
        ),
        migrations.CreateModel(
            name='Varetuttaktransaksjon',
            fields=[
                ('varetransaksjon_ptr', models.OneToOneField(to='z.Varetransaksjon', primary_key=True, auto_created=True, serialize=False, parent_link=True)),
            ],
            options={
            },
            bases=('z.varetransaksjon',),
        ),
        migrations.CreateModel(
            name='Vareuttak',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('tidspunk', models.DateTimeField(verbose_name='Tidspunkt for uttak')),
                ('beskrivelse', models.TextField(verbose_name='Beskrivelse av uttak')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Zrapport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nummer', models.PositiveIntegerField(verbose_name='Zrapport-nummer')),
                ('tidspunkt', models.DateTimeField(verbose_name='Tidspunkt')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='varetuttaktransaksjon',
            name='vareuttak',
            field=models.ForeignKey(to='z.Vareuttak', related_name='transaksjoner'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='varetransaksjon',
            name='salgsvare',
            field=models.ForeignKey(to='varer.Salgsvare', related_name='transaksjoner'),
            preserve_default=True,
        ),
    ]
