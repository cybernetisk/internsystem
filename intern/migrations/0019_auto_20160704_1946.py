# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('intern', '0018_auto_20160704_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intern',
            name='member',
            field=models.ForeignKey(blank=True, to='members.Member', null=True),
        ),
    ]
