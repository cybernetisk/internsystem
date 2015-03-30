# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skitur', '0002_auto_20150331_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='cabin',
            field=models.ForeignKey(to='skitur.Cabin', null=True, blank=True, related_name='participants'),
            preserve_default=True,
        ),
    ]
