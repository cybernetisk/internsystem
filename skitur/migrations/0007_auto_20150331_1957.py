# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import skitur.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('skitur', '0006_auto_20150331_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='phone',
            field=skitur.fields.PhoneField(validators=[django.core.validators.RegexValidator(regex='^\\+?[1-9]\\d{1,14}$', message='Must be a valid E.164 phone number.')], verbose_name='Phone number', max_length=16),
            preserve_default=True,
        ),
    ]
