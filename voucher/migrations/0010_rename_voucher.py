# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('voucher', '0009_uselog_issuing_user'),
    ]

    operations = [
        migrations.RenameModel('Wallet', 'VoucherWallet'),
        migrations.RenameModel('UseLog', 'VoucherUseLog'),

        migrations.AlterField(
            model_name='worklog',
            name='wallet',
            field=models.ForeignKey(to='voucher.VoucherWallet', related_name='worklogs', on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='voucheruselog',
            name='wallet',
            field=models.ForeignKey(to='voucher.VoucherWallet', related_name='uselogs', on_delete=models.CASCADE),
        ),
        migrations.AlterUniqueTogether(
            name='voucherwallet',
            unique_together=set([('user', 'semester')]),
        ),
    ]
