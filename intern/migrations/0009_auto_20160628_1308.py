# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0005_user_phone_number'),
        ('intern', '0008_auto_20160628_1259'),
    ]

    operations = [
        migrations.CreateModel(
            name='InternRole',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='intern',
            unique_together=set([]),
        ),
        migrations.AddField(
            model_name='internrole',
            name='intern',
            field=models.ForeignKey(to='intern.Intern'),
        ),
        migrations.AddField(
            model_name='internrole',
            name='role',
            field=models.ForeignKey(to='intern.Role'),
        ),
        migrations.AddField(
            model_name='internrole',
            name='semester_end',
            field=models.ForeignKey(related_name='end', to='core.Semester'),
        ),
        migrations.AddField(
            model_name='internrole',
            name='semester_start',
            field=models.ForeignKey(related_name='start', to='core.Semester'),
        ),
        migrations.RemoveField(
            model_name='intern',
            name='roles',
        ),
        migrations.RemoveField(
            model_name='intern',
            name='semester',
        ),
    ]
