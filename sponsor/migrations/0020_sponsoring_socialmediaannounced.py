# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("sponsor", "0019_auto_20160414_0027"),
    ]

    operations = [
        migrations.AddField(
            model_name="sponsoring",
            name="socialMediaAnnounced",
            field=models.BooleanField(
                default=False, verbose_name="Social media announcements were made"
            ),
            preserve_default=True,
        ),
    ]
