# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('members', '0009_member_last_edited_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interngroup',
            name='leader',
        ),
        migrations.RemoveField(
            model_name='internmember',
            name='member',
        ),
        migrations.RemoveField(
            model_name='internmember',
            name='roles',
        ),
        migrations.RemoveField(
            model_name='internmember',
            name='semester',
        ),
        migrations.RemoveField(
            model_name='internmember',
            name='user',
        ),
        migrations.RemoveField(
            model_name='internrole',
            name='role_groups',
        ),
        migrations.DeleteModel(
            name='InternGroup',
        ),
        migrations.DeleteModel(
            name='InternMember',
        ),
        migrations.DeleteModel(
            name='InternRole',
        ),
    ]
