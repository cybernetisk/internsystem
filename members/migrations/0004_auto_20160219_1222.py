# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        ('members', '0003_member_uio_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='date_lifetime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='user',
            field=models.ForeignKey(null=True, related_name='member', to=settings.AUTH_USER_MODEL, blank=True, on_delete=models.CASCADE),
        ),
    ]
