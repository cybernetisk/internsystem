# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.utils


class Migration(migrations.Migration):

    dependencies = [
        ('intern', '0017_auto_20160704_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internrole',
            name='semester_start',
            field=models.ForeignKey(default=core.utils.get_semester, to='core.Semester', related_name='start'),
        ),
    ]
