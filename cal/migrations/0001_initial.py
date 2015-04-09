# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('start', models.DateTimeField(verbose_name='Start time of the event')),
                ('end', models.DateTimeField(verbose_name='End time of the event')),
                ('is_allday', models.BooleanField(default=False, verbose_name='Is this an all-day event?')),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True)),
                ('is_public', models.BooleanField(default=False, verbose_name='Public (event will be visible on cyb.no)')),
                ('is_rented', models.BooleanField(default=False, verbose_name='Rental')),
                ('in_escape', models.BooleanField(default=True, verbose_name='In Escape')),
                ('is_cancelled', models.BooleanField(default=False, verbose_name='Event has been cancelled')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
