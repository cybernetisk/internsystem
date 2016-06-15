# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('intern', '0006_auto_20160615_1557'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='internrole',
            unique_together=set([]),
        ),
    ]
