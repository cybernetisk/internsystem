# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('intern', '0015_auto_20160629_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internrole',
            name='semester_end',
            field=models.ForeignKey(to='core.Semester', null=True, blank=True, related_name='end'),
        ),
    ]
