# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0005_user_phone_number'),
        ('intern', '0002_auto_20160315_2131'),
    ]

    operations = [
        migrations.CreateModel(
            name='InternAccess',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('given_access', models.BooleanField(default=False)),
                ('card', models.ForeignKey(to='core.Card')),
            ],
        ),
        migrations.RemoveField(
            model_name='intern',
            name='given_access',
        ),
        migrations.AddField(
            model_name='intern',
            name='access',
            field=models.ManyToManyField(to='intern.InternAccess'),
        ),
    ]
