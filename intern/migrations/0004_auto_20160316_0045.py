# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0005_user_phone_number'),
        ('intern', '0003_auto_20160316_0012'),
    ]

    operations = [
        migrations.CreateModel(
            name='InternAccessCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('given_access', models.BooleanField(default=False)),
                ('valid', models.BooleanField(default=True)),
                ('card', models.ForeignKey(to='core.Card')),
            ],
        ),
        migrations.RemoveField(
            model_name='internaccess',
            name='card',
        ),
        migrations.RemoveField(
            model_name='intern',
            name='access',
        ),
        migrations.DeleteModel(
            name='InternAccess',
        ),
        migrations.AddField(
            model_name='internaccesscard',
            name='intern',
            field=models.ForeignKey(related_name='cards', to='intern.Intern'),
        ),
    ]
