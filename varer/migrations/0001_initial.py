# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Leverandør',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('navn', models.CharField(max_length=100)),
                ('kommentar', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Råvare',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('kategori', models.CharField(max_length=50)),
                ('navn', models.CharField(max_length=100)),
                ('mengde', models.FloatField()),
                ('mengde_svinn', models.FloatField()),
                ('enhet', models.CharField(max_length=20)),
                ('innkjøpskonto', models.PositiveSmallIntegerField()),
                ('status', models.CharField(default='OK', max_length=10, choices=[('OK', 'I bruk'), ('OLD', 'Utgått')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Råvarepris',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('bestillingskode', models.CharField(max_length=30)),
                ('pris', models.FloatField(help_text='Pris eks mva')),
                ('dato', models.DateField()),
                ('leverandør', models.ForeignKey(to='varer.Leverandør', related_name='priser', on_delete=models.CASCADE)),
                ('råvare', models.ForeignKey(to='varer.Råvare', related_name='priser', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Salgskalkyle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('navn', models.CharField(max_length=30)),
                ('kommentar', models.TextField()),
                ('dato', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SalgskalkyleVare',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('interngrad', models.FloatField(null=True)),
                ('antall', models.PositiveIntegerField()),
                ('kalkyle', models.ForeignKey(to='varer.Salgskalkyle', related_name='varer', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Salgsvare',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('kategori', models.CharField(max_length=50)),
                ('navn', models.CharField(max_length=100)),
                ('salgskonto', models.PositiveSmallIntegerField()),
                ('status', models.CharField(default='OK', max_length=10, choices=[('OK', 'I bruk'), ('OLD', 'Utgått')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SalgsvarePris',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('status', models.CharField(default='FOR', max_length=3, choices=[('FOR', 'Forslag'), ('GOD', 'Godkjent forslag'), ('KAS', 'Registrert i kasse')])),
                ('dato', models.DateField()),
                ('mva', models.PositiveSmallIntegerField()),
                ('kassenr', models.PositiveSmallIntegerField(help_text='Nr i varekatalog i kassa')),
                ('pris_intern', models.PositiveSmallIntegerField(help_text='Internpris INK mva')),
                ('pris_ekstern', models.PositiveSmallIntegerField(help_text='Eksternpris INK mva')),
                ('salgsvare', models.ForeignKey(to='varer.Salgsvare', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SalgsvareRåvare',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('mengde', models.FloatField()),
                ('råvare', models.ForeignKey(to='varer.Råvare', on_delete=models.CASCADE)),
                ('salgsvare', models.ForeignKey(to='varer.Salgsvare', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Varetelling',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('tittel', models.CharField(max_length=50)),
                ('kommentar', models.TextField()),
                ('tid', models.DateTimeField()),
                ('ansvarlig', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VaretellingVare',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('sted', models.CharField(max_length=50)),
                ('antall', models.FloatField()),
                ('kommentar', models.CharField(max_length=150)),
                ('råvare', models.ForeignKey(to='varer.Råvare', on_delete=models.CASCADE)),
                ('varetelling', models.ForeignKey(to='varer.Varetelling', related_name='varer', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='salgskalkylevare',
            name='salgsvare',
            field=models.ForeignKey(to='varer.Salgsvare', related_name='kalkyler', on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
