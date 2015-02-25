# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('varer', '0016_auto_20141227_0243'),
    ]

    operations = [
        migrations.CreateModel(
            name='KassenavnMapping',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nummer', models.PositiveSmallIntegerField(verbose_name='Nummer i kassa')),
                ('navn', models.CharField(verbose_name='Navn i kassa', max_length=15)),
                ('salgsvare', models.ForeignKey(related_name='kassenavn_mappinger', to='varer.Salgsvare')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Kvittering',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
                ('varetransaksjon_ptr', models.OneToOneField(to='z.Varetransaksjon', auto_created=True, serialize=False, primary_key=True, parent_link=True)),
            ],
            options={
            },
            bases=('z.varetransaksjon',),
        ),
        migrations.CreateModel(
            name='Varetuttaktransaksjon',
            fields=[
                ('varetransaksjon_ptr', models.OneToOneField(to='z.Varetransaksjon', auto_created=True, serialize=False, primary_key=True, parent_link=True)),
            ],
            options={
            },
            bases=('z.varetransaksjon',),
        ),
        migrations.CreateModel(
            name='Vareuttak',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
            field=models.ForeignKey(related_name='transaksjoner', to='z.Vareuttak'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='varetransaksjon',
            name='salgsvare',
            field=models.ForeignKey(related_name='transaksjoner', to='varer.Salgsvare'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='kvittering',
            name='zrapport',
            field=models.ForeignKey(related_name='kvitteringer', to='z.Zrapport'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='kassetransaksjon',
            name='kvittering',
            field=models.ForeignKey(related_name='transaksjoner', to='z.Kvittering'),
            preserve_default=True,
        ),
    ]
