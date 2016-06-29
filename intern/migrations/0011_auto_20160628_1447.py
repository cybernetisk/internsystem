# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('intern', '0010_auto_20160628_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internrole',
            name='role',
            field=models.ForeignKey(to='intern.Role', related_name='role'),
        ),
    ]
