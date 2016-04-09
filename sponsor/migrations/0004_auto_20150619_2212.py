# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0003_auto_20150619_2144'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsorcontact',
            name='address2',
            field=models.CharField(max_length=128, verbose_name='Address addition', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorcontact',
            name='billingAddress2',
            field=models.CharField(max_length=128, verbose_name='Address addition', blank=True),
            preserve_default=True,
        ),
    ]
