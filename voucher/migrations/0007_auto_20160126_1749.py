# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


sql = """UPDATE django_content_type
         SET model = 'wallet'
         WHERE model = 'voucherwallet' AND
               app_label = 'voucher';"""

reverse_sql = """UPDATE django_content_type
                 SET model = 'voucherwallet'
                 WHERE model = 'wallet' AND
                       app_label = 'voucher';"""

class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_card'),
        ('voucher', '0006_auto_20160126_1732'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='VoucherWallet',
            new_name='Wallet'
        ),
        migrations.RunSQL(sql, reverse_sql),
    ]
