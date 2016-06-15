# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('intern', '0005_auto_20160419_1459'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='intern',
            unique_together=set([('user', 'semester')]),
        ),
        migrations.AlterUniqueTogether(
            name='internrole',
            unique_together=set([('name',)]),
        ),
    ]
