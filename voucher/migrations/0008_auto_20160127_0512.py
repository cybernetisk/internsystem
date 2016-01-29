# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from voucher.models import Wallet


def fix_balance(apps, schema_editor):
    print(repr(Wallet))
    for wallet in Wallet.objects.all():
        print(repr(vars(wallet)))
        wallet.calculate_balance()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('voucher', '0007_auto_20160126_1749'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wallet',
            options={'ordering': ['user__username']},
        ),
        migrations.AddField(
            model_name='wallet',
            name='cached_hours',
            field=models.DecimalField(max_digits=8, default=0, decimal_places=2, editable=False),
        ),
        migrations.AddField(
            model_name='wallet',
            name='cached_vouchers',
            field=models.DecimalField(max_digits=8, default=0, decimal_places=2, editable=False),
        ),
        migrations.AddField(
            model_name='wallet',
            name='cached_vouchers_used',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.RunPython(fix_balance, noop)
    ]
