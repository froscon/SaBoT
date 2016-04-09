# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0013_auto_20160203_0114'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsoring',
            name='programAdTextOptOut',
            field=models.BooleanField(default=False, verbose_name='Sponsor does not use program ad text'),
            preserve_default=True,
        ),
    ]
