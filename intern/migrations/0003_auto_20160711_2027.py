# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('intern', '0002_auto_20160711_2026'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='internrole',
            unique_together=set([('intern', 'role', 'semester_start')]),
        ),
    ]
