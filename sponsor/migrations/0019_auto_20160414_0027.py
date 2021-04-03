# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("sponsor", "0018_auto_20160208_2036"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="sponsorparcel",
            name="sponsoring",
        ),
        migrations.DeleteModel(
            name="SponsorParcel",
        ),
    ]
