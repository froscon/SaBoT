# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("sponsor", "0006_sponsorparcel_createdate"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="sponsorparcel",
            name="owner",
        ),
    ]
