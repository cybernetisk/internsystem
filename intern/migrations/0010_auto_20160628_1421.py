# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('intern', '0009_auto_20160628_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internrole',
            name='intern',
            field=models.ForeignKey(related_name='roles', to='intern.Intern'),
        ),
    ]
