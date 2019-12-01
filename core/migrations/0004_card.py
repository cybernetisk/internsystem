# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150628_0504'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('comment', models.CharField(blank=True, max_length=20)),
                ('disabled', models.BooleanField(default=False)),
                ('card_number', models.CharField(unique=True, max_length=20, validators=[django.core.validators.RegexValidator('^\\d{6}\\.\\d{2}\\.\\d{7}(\\.\\d)?$', 'Enter a valid card number.', 'invalid')])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
    ]
