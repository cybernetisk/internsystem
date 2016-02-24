# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('members', '0007_member_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='uio_username',
            field=models.CharField(max_length=15, null=True, blank=True),
        ),
    ]
