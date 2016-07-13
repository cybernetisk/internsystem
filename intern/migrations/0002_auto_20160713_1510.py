# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20160713_1508'),
        ('intern', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='internrole',
            name='semesters',
            field=models.ManyToManyField(related_name='internroles', to='core.Semester'),
        ),
        migrations.AlterField(
            model_name='internrole',
            name='date_added',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterUniqueTogether(
            name='internrole',
            unique_together=set([('intern', 'role')]),
        ),
        migrations.RemoveField(
            model_name='internrole',
            name='semester_end',
        ),
        migrations.RemoveField(
            model_name='internrole',
            name='semester_start',
        ),
    ]
