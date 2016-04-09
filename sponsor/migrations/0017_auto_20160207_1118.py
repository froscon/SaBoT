# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0016_auto_20160205_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsorpackage',
            name='additionalContentTextDE',
            field=models.TextField(verbose_name='Additional package contents (German). See English', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorpackage',
            name='additionalContentTextEN',
            field=models.TextField(verbose_name='Additional package content (English). Additional items that belong to this package but are not automatically generated from the selections above.', blank=True),
            preserve_default=True,
        ),
    ]
