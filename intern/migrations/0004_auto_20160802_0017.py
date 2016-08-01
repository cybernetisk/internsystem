# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-01 22:17
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('intern', '0003_auto_20160729_2244'),
    ]

    operations = [
        migrations.AddField(
            model_name='internrole',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='internroles_created', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='internrole',
            name='date_edited',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2016, 8, 1, 22, 17, 0, 399873, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='internrole',
            name='last_editor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='internroles_edited', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='internrole',
            name='removed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='internroles_removed', to=settings.AUTH_USER_MODEL),
        ),
    ]
