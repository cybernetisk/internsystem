# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('skitur', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='phone',
            field=models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(message='Must be a valid E.164 phone number.', regex='^\\+?[1-9]\\d{1,14}$')], verbose_name='Phone number'),
            preserve_default=True,
        ),
    ]
