# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("invoice", "0003_auto_20160207_1343"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invoice",
            name="invoiceAmount",
            field=models.DecimalField(
                verbose_name="Invoice amount", max_digits=32, decimal_places=2
            ),
            preserve_default=True,
        ),
    ]
