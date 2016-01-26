# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


sql = """UPDATE django_content_type
         SET model = 'uselog'
         WHERE model = 'voucheruselog' AND
               app_label = 'voucher';"""

reverse_sql = """UPDATE django_content_type
                 SET model = 'voucheruselog'
                 WHERE model = 'uselog' AND
                       app_label = 'voucher';"""


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0005_auto_20160126_1721'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='VoucherUseLog',
            new_name='UseLog',
        ),
        migrations.RunSQL(sql, reverse_sql),
    ]
