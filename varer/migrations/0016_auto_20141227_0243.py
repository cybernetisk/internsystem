# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('varer', '0015_auto_20141224_0052'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='råvare',
            options={'ordering': ['innkjopskonto__gruppe', 'kategori', 'navn'], 'verbose_name_plural': 'råvarer'},
        ),
        migrations.AlterModelOptions(
            name='salgsvare',
            options={'ordering': ['salgskonto__gruppe', 'kategori', 'navn'], 'verbose_name_plural': 'salgsvarer'},
        ),
        migrations.AddField(
            model_name='varetellingvare',
            name='antallpant',
            field=models.FloatField(blank=True, help_text='Antall hele forpakninger det skal telles pant for, brukes vanlig antall (avrundet opp) hvis ikke spesifisert', null=True),
            preserve_default=True,
        ),
    ]
