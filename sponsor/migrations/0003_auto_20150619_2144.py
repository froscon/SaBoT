# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("sponsor", "0002_sponsoring_recruitinginfo"),
    ]

    operations = [
        migrations.AddField(
            model_name="sponsorcontact",
            name="billingAddress2",
            field=models.CharField(
                max_length=128, verbose_name="Additional address line", blank=True
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="sponsorcontact",
            name="billingCity",
            field=models.CharField(max_length=64, verbose_name="City", blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="sponsorcontact",
            name="billingCountry",
            field=models.CharField(max_length=64, verbose_name="Country", blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="sponsorcontact",
            name="billingName",
            field=models.CharField(
                max_length=128, verbose_name="Person or department", blank=True
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="sponsorcontact",
            name="billingStreet",
            field=models.CharField(max_length=128, verbose_name="Street", blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="sponsorcontact",
            name="billingZipcode",
            field=models.CharField(max_length=16, verbose_name="ZIP Code", blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="sponsorcontact",
            name="differentBillingAddress",
            field=models.BooleanField(
                default=False, verbose_name="Use different billing address"
            ),
            preserve_default=True,
        ),
    ]
