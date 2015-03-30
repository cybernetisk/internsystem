# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skitur', '0003_auto_20150331_0007'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='trip',
            field=models.ForeignKey(default=1, related_name='participants', to='skitur.Trip'),
            preserve_default=False,
        ),
    ]
