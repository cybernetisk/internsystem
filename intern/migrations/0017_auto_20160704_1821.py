# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('intern', '0016_auto_20160704_1317'),
    ]

    operations = [
        migrations.AddField(
            model_name='internrole',
            name='date_access_given',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='internrole',
            name='date_added',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
