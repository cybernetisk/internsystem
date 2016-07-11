# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_nfccard'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=20)),
                ('uio_name', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Intern',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('active', models.BooleanField(default=True)),
                ('comments', models.CharField(null=True, max_length=300, blank=True)),
                ('user', models.ForeignKey(unique=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InternGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(null=True, max_length=300, blank=True)),
                ('leader', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InternRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('comments', models.CharField(null=True, max_length=300, blank=True)),
                ('date_added', models.DateField(default=django.utils.timezone.now)),
                ('date_removed', models.DateField(null=True, blank=True)),
                ('date_access_given', models.DateField(null=True, blank=True)),
                ('date_access_revoked', models.DateField(null=True, blank=True)),
                ('intern', models.ForeignKey(related_name='roles', to='intern.Intern')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(null=True, max_length=300, blank=True)),
                ('access_levels', models.ManyToManyField(to='intern.AccessLevel')),
                ('groups', models.ManyToManyField(related_name='roles', to='intern.InternGroup')),
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
            field=models.ForeignKey(to='core.Semester', null=True, related_name='end', blank=True),
        ),
        migrations.AddField(
            model_name='internrole',
            name='semester_start',
            field=models.ForeignKey(related_name='start', to='core.Semester'),
        ),
        migrations.AlterUniqueTogether(
            name='internrole',
            unique_together=set([('intern', 'role', 'semester_start')]),
        ),
    ]
