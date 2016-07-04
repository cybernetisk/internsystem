# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_nfccard'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nfccard',
            name='user',
        ),
        migrations.AddField(
            model_name='card',
            name='card_uid',
            field=models.CharField(null=True, unique=True, max_length=8, blank=True, validators=[django.core.validators.RegexValidator('^[a-z0-9]{8}$', 'Enter valid card uid.', 'invalid')]),
        ),
        migrations.AlterField(
            model_name='card',
            name='card_number',
            field=models.CharField(null=True, unique=True, max_length=20, blank=True, validators=[django.core.validators.RegexValidator('^\\d{6}\\.\\d{2}\\.\\d{7}(\\.\\d)?$', 'Enter a valid card number.', 'invalid')]),
        ),
        migrations.AlterField(
            model_name='card',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, blank=True),
        ),
        migrations.DeleteModel(
            name='NfcCard',
        ),
    ]
