# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('varer', '0018_auto_20160128_2303'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='varetellingvare',
            options={'ordering': ['varetelling', '-time_added']},
        ),
        migrations.AddField(
            model_name='varetelling',
            name='is_locked',
            field=models.BooleanField(default=False, help_text='Sperr tellingen for endringer'),
        ),
        migrations.AlterField(
            model_name='varetellingvare',
            name='added_by',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, help_text='Brukeren som registrerte oppføringen', null=True, on_delete=models.CASCADE),
        ),
    ]
