# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('varer', '0017_salgsvare_kassenavn'),
    ]

    operations = [
        migrations.AddField(
            model_name='varetellingvare',
            name='added_by',
            field=models.ForeignKey(help_text='Brukeren som registrerte oppføringen', null=True, to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='varetellingvare',
            name='time_added',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 1, 28, 22, 3, 18, 828239, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='varetellingvare',
            name='time_price',
            field=models.DateTimeField(blank=True, help_text='Overstyring av tidspunkt varen skal prises', null=True),
        ),
        migrations.AlterField(
            model_name='varetellingvare',
            name='sted',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
