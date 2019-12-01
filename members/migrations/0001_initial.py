# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_card'),
    ]

    operations = [
        migrations.CreateModel(
            name='InternGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=300)),
                ('leader', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='InternMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('recivedCard', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('comments', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='InternRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=300)),
                ('role_groups', models.ManyToManyField(related_name='groups', to='members.InternGroup')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('lifetime', models.BooleanField(help_text='Lifetime member')),
                ('honorary', models.BooleanField(help_text='Honorary member')),
                ('date_joined', models.DateTimeField()),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('seller', models.ForeignKey(related_name='seller', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
                ('semester', models.ForeignKey(to='core.Semester', on_delete=models.CASCADE)),
                ('user', models.ForeignKey(related_name='user', blank=True, to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
        migrations.AddField(
            model_name='internmember',
            name='member',
            field=models.ForeignKey(to='members.Member', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='internmember',
            name='roles',
            field=models.ManyToManyField(related_name='roles', to='members.InternRole'),
        ),
        migrations.AddField(
            model_name='internmember',
            name='semester',
            field=models.ForeignKey(to='core.Semester', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='internmember',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
        migrations.AlterUniqueTogether(
            name='member',
            unique_together=set([('name', 'email', 'semester')]),
        ),
    ]
