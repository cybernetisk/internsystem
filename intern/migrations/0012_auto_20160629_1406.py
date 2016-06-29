# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('intern', '0011_auto_20160628_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='internrole',
            name='comments',
            field=models.CharField(null=True, max_length=300, blank=True),
        ),
        migrations.AlterField(
            model_name='internrole',
            name='semester_end',
            field=models.ForeignKey(to='core.Semester', related_name='end', null=True),
        ),
    ]
