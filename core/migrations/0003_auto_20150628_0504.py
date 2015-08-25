# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150604_0016'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='semester',
            options={'ordering': ['-year', '-semester']},
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', core.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='email address', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(related_name='user_set', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(null=True, verbose_name='last login', blank=True),
        ),
    ]
