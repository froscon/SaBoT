# -*- coding: utf-8 -*-


from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ("sponsor", "0005_sponsorparcel"),
    ]

    operations = [
        migrations.AddField(
            model_name="sponsorparcel",
            name="createDate",
            field=models.DateField(
                default=datetime.datetime(2015, 6, 19, 21, 32, 24, 822951, tzinfo=datetime.timezone.utc),
                auto_now_add=True,
            ),
            preserve_default=False,
        ),
    ]
