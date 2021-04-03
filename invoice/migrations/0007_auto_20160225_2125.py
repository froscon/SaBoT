# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("invoice", "0006_auto_20160213_1752"),
    ]

    operations = [
        migrations.AlterField(
            model_name="documenttemplate",
            name="template",
            field=models.FileField(
                upload_to=b"invoice_templates",
                verbose_name="Invoice template file (odt)",
            ),
            preserve_default=True,
        ),
    ]
