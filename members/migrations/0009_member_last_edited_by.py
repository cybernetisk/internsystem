# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('members', '0008_auto_20160225_0000'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='last_edited_by',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, related_name='modifier'),
        ),
    ]
