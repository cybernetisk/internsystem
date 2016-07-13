# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_nfccard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nfccard',
            name='card_uid',
            field=models.CharField(max_length=8, validators=[django.core.validators.RegexValidator('^[a-f0-9]{4,}$', 'Enter valid card uid.', 'invalid')], unique=True),
        ),
    ]
