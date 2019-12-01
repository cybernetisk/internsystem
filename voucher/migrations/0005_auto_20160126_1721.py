# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0004_auto_20160124_2143'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='voucheruselog',
            options={'ordering': ['-date_spent']},
        ),
        migrations.AlterModelOptions(
            name='worklog',
            options={'ordering': ['-date_issued']},
        ),
        migrations.AlterField(
            model_name='voucheruselog',
            name='wallet',
            field=models.ForeignKey(related_name='uselogs', to='voucher.VoucherWallet', on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='worklog',
            name='wallet',
            field=models.ForeignKey(related_name='worklogs', to='voucher.VoucherWallet', on_delete=models.CASCADE),
        ),
    ]
