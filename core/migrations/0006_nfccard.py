# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_user_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='NfcCard',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('card_uid', models.CharField(validators=[django.core.validators.RegexValidator('^[a-z0-9]{8}$', 'Enter valid card uid.', 'invalid')], max_length=8, unique=True)),
                ('intern', models.BooleanField(default=False)),
                ('comment', models.CharField(max_length=20, blank=True)),
                ('user', models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
