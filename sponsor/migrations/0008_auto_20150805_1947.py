# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0007_remove_sponsorparcel_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsoring',
            name='owner',
            field=models.ForeignKey(related_name='sponsorings', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorparcel',
            name='received',
            field=models.BooleanField(default=False, verbose_name='We received this package (tick this and enter storage location once handled)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorparcel',
            name='trackingUrl',
            field=models.URLField(verbose_name='Tracking URL (if available)', blank=True),
            preserve_default=True,
        ),
    ]
