# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("sponsor", "0023_auto_20160924_1415"),
    ]

    operations = [
        migrations.AddField(
            model_name="sponsoring",
            name="displayCompanyName",
            field=models.CharField(
                max_length=256,
                verbose_name="Company or product name that we should you to announce and advertise your sponsoring",
                blank=True,
            ),
            preserve_default=True,
        ),
    ]
