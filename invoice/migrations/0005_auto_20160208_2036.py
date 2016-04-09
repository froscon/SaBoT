# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0004_auto_20160208_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoiceAmount',
            field=models.DecimalField(verbose_name='Invoice amount', editable=False, max_digits=32, decimal_places=2),
            preserve_default=True,
        ),
    ]
