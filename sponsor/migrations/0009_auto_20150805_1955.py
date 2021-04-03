# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0008_auto_20150805_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsoring',
            name='owner',
            field=models.ForeignKey(related_name='sponsorings', editable=False, to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsorparcel',
            name='sponsoring',
            field=models.ForeignKey(related_name='parcels', to='sponsor.Sponsoring', on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
