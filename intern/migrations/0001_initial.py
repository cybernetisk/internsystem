# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone
import core.utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0006_nfccard'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessLevel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('uio_name', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Intern',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('comments', models.CharField(max_length=300, null=True, blank=True)),
                ('user', models.ForeignKey(unique=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InternGroup',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=300, null=True, blank=True)),
                ('leader', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InternRole',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('comments', models.CharField(max_length=300, null=True, blank=True)),
                ('date_added', models.DateField(default=django.utils.timezone.now)),
                ('date_access_given', models.DateField(null=True, blank=True)),
                ('intern', models.ForeignKey(related_name='roles', to='intern.Intern')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=300, null=True, blank=True)),
                ('access_levels', models.ManyToManyField(to='intern.AccessLevel')),
                ('groups', models.ManyToManyField(to='intern.InternGroup', related_name='roles')),
            ],
        ),
        migrations.AddField(
            model_name='internrole',
            name='role',
            field=models.ForeignKey(related_name='intern', to='intern.Role'),
        ),
        migrations.AddField(
            model_name='internrole',
            name='semester_end',
            field=models.ForeignKey(to='core.Semester', related_name='end', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='internrole',
            name='semester_start',
            field=models.ForeignKey(to='core.Semester', related_name='start', default=core.utils.get_semester),
        ),
    ]
