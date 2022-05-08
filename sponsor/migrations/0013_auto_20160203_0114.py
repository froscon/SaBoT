# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("sponsor", "0012_auto_20160203_0051"),
    ]

    operations = [
        migrations.RenameField(
            model_name="sponsoring",
            old_name="facebookPaceOptOut",
            new_name="facebookPageOptOut",
        ),
    ]
