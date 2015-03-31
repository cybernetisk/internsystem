# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import skitur.fields


class Migration(migrations.Migration):

    dependencies = [
        ('skitur', '0007_auto_20150331_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='phone',
            field=skitur.fields.PhoneField(max_length=16, verbose_name='Phone number'),
            preserve_default=True,
        ),
    ]
