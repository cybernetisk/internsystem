# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_nfccard'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('voucher', '0010_rename_voucher'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoffeeUseLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('date_spent', models.DateTimeField(auto_now_add=True)),
                ('comment', models.CharField(blank=True, max_length=100, null=True)),
                ('vouchers', models.IntegerField()),
                ('issuing_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_spent'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CoffeeWallet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('cached_balance', models.DecimalField(max_digits=8, decimal_places=2, editable=False, default=0)),
                ('cached_vouchers', models.DecimalField(max_digits=8, decimal_places=2, editable=False, default=0)),
                ('cached_vouchers_used', models.IntegerField(editable=False, default=0)),
                ('card', models.ForeignKey(to='core.NfcCard')),
                ('semester', models.ForeignKey(to='core.Semester')),
            ],
            options={
                'ordering': ['card__card_uid'],
            },
        ),
        migrations.CreateModel(
            name='CoffeeRegisterLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('date_issued', models.DateTimeField(auto_now_add=True)),
                ('comment', models.CharField(blank=True, max_length=100, null=True)),
                ('vouchers', models.DecimalField(decimal_places=2, max_digits=8)),
                ('issuing_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('wallet', models.ForeignKey(to='voucher.CoffeeWallet', related_name='registerlogs')),
            ],
            options={
                'ordering': ['-date_issued'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='coffeeuselog',
            name='wallet',
            field=models.ForeignKey(to='voucher.CoffeeWallet', related_name='uselogs'),
        ),
        migrations.AlterUniqueTogether(
            name='coffeewallet',
            unique_together=set([('card', 'semester')]),
        ),
    ]
