# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_card'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoucherUseLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date_spent', models.DateTimeField(auto_now_add=True)),
                ('comment', models.CharField(max_length=100)),
                ('vouchers', models.DecimalField(decimal_places=0, max_digits=3)),
            ],
        ),
        migrations.CreateModel(
            name='VoucherWallet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('cached_balance', models.DecimalField(decimal_places=2, max_digits=8, editable=False, default=0)),
                ('semester', models.ForeignKey(to='core.Semester', on_delete=models.CASCADE)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='WorkLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date_issued', models.DateTimeField(auto_now_add=True)),
                ('date_worked', models.DateField()),
                ('work_group', models.CharField(max_length=20)),
                ('hours', models.DecimalField(decimal_places=1, max_digits=8)),
                ('vouchers', models.DecimalField(decimal_places=2, max_digits=8)),
                ('comment', models.CharField(max_length=100)),
                ('issuing_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
                ('wallet', models.ForeignKey(to='voucher.VoucherWallet', on_delete=models.CASCADE)),
            ],
        ),
        migrations.AddField(
            model_name='voucheruselog',
            name='wallet',
            field=models.ForeignKey(to='voucher.VoucherWallet', on_delete=models.CASCADE),
        ),
        migrations.AlterUniqueTogether(
            name='voucherwallet',
            unique_together=set([('user', 'semester')]),
        ),
    ]
