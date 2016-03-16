# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0005_user_phone_number'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('members', '0010_auto_20160315_2114'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessLevel',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=20)),
                ('uio_name', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Intern',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('recived_card', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('comments', models.CharField(max_length=300)),
                ('given_access', models.BooleanField(default=False)),
                ('member', models.ForeignKey(to='members.Member')),
            ],
        ),
        migrations.CreateModel(
            name='InternGroup',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=300)),
                ('leader', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InternRole',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=300)),
                ('access_levels', models.ManyToManyField(to='intern.AccessLevel')),
                ('groups', models.ManyToManyField(to='intern.InternGroup', related_name='groups')),
            ],
        ),
        migrations.AddField(
            model_name='intern',
            name='roles',
            field=models.ManyToManyField(to='intern.InternRole', related_name='roles'),
        ),
        migrations.AddField(
            model_name='intern',
            name='semester',
            field=models.ForeignKey(to='core.Semester'),
        ),
        migrations.AddField(
            model_name='intern',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
