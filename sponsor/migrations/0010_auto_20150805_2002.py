# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("sponsor", "0009_auto_20150805_1955"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sponsorparcel",
            name="sponsoring",
            field=models.ForeignKey(
                related_name="parcels",
                blank=True,
                to="sponsor.Sponsoring",
                null=True,
                on_delete=models.CASCADE,
            ),
            preserve_default=True,
        ),
    ]
