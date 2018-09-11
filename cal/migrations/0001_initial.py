# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(verbose_name='Start time of the event')),
                ('end', models.DateTimeField(verbose_name='End time of the event')),
                ('is_allday', models.BooleanField(default=False, verbose_name='Is this an all-day event?')),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True)),
                ('comment', models.TextField(blank=True, verbose_name='Non-public comment')),
                ('link', models.CharField(blank=True, max_length=256, null=True)),
                ('is_published', models.BooleanField(default=False, verbose_name='Event is published (specially shown on intern, never public)')),
                ('is_public', models.BooleanField(default=False, verbose_name='Public (event will be visible on cyb.no)')),
                ('is_external', models.BooleanField(default=False, verbose_name='External event, not associated with CYB')),
                ('in_escape', models.BooleanField(default=True, verbose_name='Occupies Escape')),
                ('is_cancelled', models.BooleanField(default=False, verbose_name='Event has been cancelled')),
                ('organizer', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, blank=True, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
