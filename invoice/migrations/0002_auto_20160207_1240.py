# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("invoice", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="invoice",
            name="payed",
            field=models.BooleanField(
                default=False, verbose_name="This invoice is payed."
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="invoicetemplate",
            name="template",
            field=models.FileField(
                upload_to=b"invoice_templates",
                null=True,
                verbose_name="Invoice template file (odt)",
                blank=True,
            ),
            preserve_default=True,
        ),
    ]
