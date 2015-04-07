# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skitur', '0008_auto_20150331_2138'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='participant',
            unique_together=set([('trip', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='wish',
            unique_together=set([('participant', 'wish')]),
        ),
    ]
