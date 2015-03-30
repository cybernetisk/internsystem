# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cabin',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='Cabin name', max_length=128)),
                ('beds', models.PositiveSmallIntegerField(verbose_name='Number of beds in the cabin')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('has_payed', models.BooleanField(verbose_name='Payment has been received.', default=False)),
                ('has_cancelled', models.BooleanField(verbose_name='Participant has cancelled the registration', default=False)),
                ('notes', models.TextField(blank=True, default='')),
                ('phone', models.CharField(verbose_name='Phone number', max_length=16)),
                ('registration_time', models.DateTimeField(verbose_name='Registration time', auto_now_add=True)),
                ('affiliation', models.CharField(verbose_name='Ifi affiliation', default='NO', max_length=2, choices=[('ST', 'Student'), ('AL', 'Alumnus'), ('NO', 'None')])),
                ('cabin', models.ForeignKey(to='skitur.Cabin', null=True, related_name='participants')),
                ('user', models.ForeignKey(related_name='trip_participations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date', models.DateField(verbose_name='Start date of the trip')),
                ('places', models.PositiveSmallIntegerField(verbose_name='Number of places on the trip')),
                ('description', models.TextField(verbose_name='Trip description. Used on the signup form.')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Wish',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('participant', models.ForeignKey(related_name='wishes', to='skitur.Participant')),
                ('wish', models.ForeignKey(related_name='wished_by', to='skitur.Participant')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='cabin',
            name='trip',
            field=models.ForeignKey(related_name='cabins', to='skitur.Trip'),
            preserve_default=True,
        ),
    ]
