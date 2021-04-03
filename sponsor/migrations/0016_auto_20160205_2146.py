# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("sponsor", "0015_auto_20160205_1940"),
    ]

    operations = [
        migrations.AddField(
            model_name="sponsoring",
            name="billingReferenceOptOut",
            field=models.BooleanField(
                default=False,
                verbose_name="Sponsor does not provide a billing reference number",
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="sponsoring",
            name="billingName",
            field=models.CharField(
                max_length=128,
                verbose_name="Person or department (This is the second line in the address. The first is always your company name)",
                blank=True,
            ),
            preserve_default=True,
        ),
    ]
