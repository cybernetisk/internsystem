# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('intern', '0007_auto_20160615_1558'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=300, null=True, blank=True)),
                ('access_levels', models.ManyToManyField(to='intern.AccessLevel')),
                ('groups', models.ManyToManyField(related_name='groups', to='intern.InternGroup')),
            ],
        ),
        migrations.RemoveField(
            model_name='internrole',
            name='access_levels',
        ),
        migrations.RemoveField(
            model_name='internrole',
            name='groups',
        ),
        migrations.AlterField(
            model_name='intern',
            name='roles',
            field=models.ManyToManyField(related_name='roles', to='intern.Role'),
        ),
        migrations.DeleteModel(
            name='InternRole',
        ),
    ]
