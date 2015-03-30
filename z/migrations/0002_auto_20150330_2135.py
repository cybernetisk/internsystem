# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('z', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Betalingskonto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('kontonr', models.PositiveSmallIntegerField(verbose_name='Kontonummer')),
                ('navn', models.CharField(max_length=100, verbose_name='Kontonavn')),
                ('kassenr', models.PositiveSmallIntegerField(verbose_name='Kassenummer')),
                ('kassenavn', models.CharField(max_length=15, verbose_name='Kassenavn')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Betalingstransaksjon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('beløp', models.FloatField(verbose_name='Beløp betalt')),
                ('tidspunkt', models.DateTimeField(verbose_name='Tidspunkt for transaksjon')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='KasseBetalingstransaksjon',
            fields=[
                ('betalingstransaksjon_ptr', models.OneToOneField(parent_link=True, primary_key=True, to='z.Betalingstransaksjon', serialize=False, auto_created=True)),
                ('kvittering', models.ForeignKey(to='z.Kvittering', related_name='betalinger')),
            ],
            options={
            },
            bases=('z.betalingstransaksjon',),
        ),
        migrations.AddField(
            model_name='betalingstransaksjon',
            name='betalingskonto',
            field=models.ForeignKey(to='z.Betalingskonto', related_name='transaksjoner'),
            preserve_default=True,
        ),
        migrations.RenameField(
            model_name='vareuttak',
            old_name='tidspunk',
            new_name='tidspunkt',
        ),
        migrations.AddField(
            model_name='varetransaksjon',
            name='pris',
            field=models.FloatField(help_text='Salgspris inkl. mva', default=0.0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='varetuttaktransaksjon',
            name='vareuttak',
            field=models.ForeignKey(to='z.Vareuttak', related_name='varer'),
            preserve_default=True,
        ),
    ]
