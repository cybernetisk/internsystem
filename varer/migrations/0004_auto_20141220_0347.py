# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('varer', '0003_auto_20141219_2301'),
    ]

    operations = [
        migrations.CreateModel(
            name='Konto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('innkjøpskonto', models.PositiveSmallIntegerField()),
                ('varelagerkonto', models.PositiveSmallIntegerField()),
                ('beholdningsendringskonto', models.PositiveSmallIntegerField()),
                ('salgskonto', models.PositiveSmallIntegerField()),
                ('navn', models.CharField(max_length=30)),
                ('kortnavn', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='leverandør',
            options={'ordering': ['navn'], 'verbose_name_plural': 'leverandører'},
        ),
        migrations.AlterModelOptions(
            name='råvare',
            options={'ordering': ['kategori', 'navn'], 'verbose_name_plural': 'råvarer'},
        ),
        migrations.AlterModelOptions(
            name='råvarepris',
            options={'ordering': ['-dato'], 'verbose_name_plural': 'råvarepriser'},
        ),
        migrations.AlterModelOptions(
            name='salgskalkyle',
            options={'ordering': ['-dato'], 'verbose_name_plural': 'salgskalkyler'},
        ),
        migrations.AlterModelOptions(
            name='salgskalkylevare',
            options={'ordering': ['salgsvare'], 'verbose_name_plural': 'salgskalkylevarer'},
        ),
        migrations.AlterModelOptions(
            name='salgsvare',
            options={'ordering': ['kategori', 'navn'], 'verbose_name_plural': 'salgsvarer'},
        ),
        migrations.AlterModelOptions(
            name='salgsvarepris',
            options={'ordering': ['-dato'], 'verbose_name_plural': 'salgsvarepriser'},
        ),
        migrations.AlterModelOptions(
            name='varetelling',
            options={'ordering': ['-tid'], 'verbose_name_plural': 'varetellinger'},
        ),
        migrations.AlterModelOptions(
            name='varetellingvare',
            options={'ordering': ['varetelling', 'råvare']},
        ),
        migrations.AddField(
            model_name='salgskalkyle',
            name='varer',
            field=models.ManyToManyField(through='varer.SalgskalkyleVare', to='varer.Salgsvare', related_name='salgskalkyler'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='salgsvare',
            name='råvarer',
            field=models.ManyToManyField(through='varer.SalgsvareRåvare', to='varer.Råvare', related_name='salgsvarer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='varetelling',
            name='varer',
            field=models.ManyToManyField(through='varer.VaretellingVare', to='varer.Råvare', related_name='varetellinger'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='råvare',
            name='innkjøpskonto',
            field=models.ForeignKey(to='varer.Konto', related_name='råvarer', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='salgskalkylevare',
            name='interngrad',
            field=models.FloatField(blank=True, help_text='Prosent andel (antall enheter) solgt til internpris', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='salgskalkylevare',
            name='kalkyle',
            field=models.ForeignKey(to='varer.Salgskalkyle', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='salgskalkylevare',
            name='salgsvare',
            field=models.ForeignKey(to='varer.Salgsvare', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='salgsvare',
            name='salgskonto',
            field=models.ForeignKey(to='varer.Konto', related_name='salgsvarer', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='varetellingvare',
            name='varetelling',
            field=models.ForeignKey(to='varer.Varetelling', on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
