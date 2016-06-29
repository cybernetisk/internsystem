# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('intern', '0013_auto_20160629_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intern',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='intern'),
        ),
        migrations.AlterField(
            model_name='internrole',
            name='role',
            field=models.ForeignKey(to='intern.Role', related_name='intern'),
        ),
    ]
