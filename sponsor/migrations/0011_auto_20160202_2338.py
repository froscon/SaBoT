# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("sponsor", "0010_auto_20150805_2002"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="sponsorcontact",
            options={"ordering": ["companyName"]},
        ),
        migrations.AlterModelOptions(
            name="sponsoring",
            options={"ordering": ["contact"]},
        ),
        migrations.RemoveField(
            model_name="sponsorcontact",
            name="billingAddress2",
        ),
        migrations.RemoveField(
            model_name="sponsorcontact",
            name="billingCity",
        ),
        migrations.RemoveField(
            model_name="sponsorcontact",
            name="billingCountry",
        ),
        migrations.RemoveField(
            model_name="sponsorcontact",
            name="billingName",
        ),
        migrations.RemoveField(
            model_name="sponsorcontact",
            name="billingStreet",
        ),
        migrations.RemoveField(
            model_name="sponsorcontact",
            name="billingZipcode",
        ),
        migrations.RemoveField(
            model_name="sponsorcontact",
            name="differentBillingAddress",
        ),
        migrations.RemoveField(
            model_name="sponsoring",
            name="recruitingInfo",
        ),
        migrations.AddField(
            model_name="sponsoring",
            name="billingAddress2",
            field=models.CharField(
                max_length=128, verbose_name="Address addition", blank=True
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="sponsoring",
            name="billingCity",
            field=models.CharField(max_length=64, verbose_name="City", blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="sponsoring",
            name="billingCountry",
            field=models.CharField(
                default=b"Deutschland",
                max_length=64,
                verbose_name="Country",
                blank=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="sponsoring",
            name="billingName",
            field=models.CharField(
                max_length=128, verbose_name="Person or department", blank=True
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="sponsoring",
            name="billingReference",
            field=models.CharField(
                max_length=64, verbose_name="Your reference number", blank=True
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="sponsoring",
            name="billingStreet",
            field=models.CharField(max_length=128, verbose_name="Street", blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="sponsoring",
            name="billingZipcode",
            field=models.CharField(max_length=16, verbose_name="ZIP Code", blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="sponsoring",
            name="clearedForBilling",
            field=models.BooleanField(
                default=False, verbose_name="This sponsoring is ready for billing"
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="sponsoring",
            name="recruitingInfoDE",
            field=models.TextField(
                verbose_name="What are you looking for? Only short job descriptions. Internships? Bachelor's/Master's thesis? (German)",
                blank=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="sponsoring",
            name="recruitingInfoEN",
            field=models.TextField(
                verbose_name="Your recruiting keywords (as above) in English",
                blank=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="sponsoring",
            name="vectorLogo",
            field=models.FileField(
                upload_to=b"sponsors/vec_logos",
                verbose_name="Company logo as vector graphics (preferably PDF or SVG) for printed advertisements such as posters, flyers and visitor badges",
                blank=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="sponsorpackage",
            name="providesVectorLogo",
            field=models.BooleanField(
                default=False,
                verbose_name="The sponsor should upload its logo as vector graphics",
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="sponsoring",
            name="logo",
            field=models.ImageField(
                upload_to=b"sponsors/logos",
                verbose_name="Company logo for homepage (preferably as PNG)",
                blank=True,
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="sponsoring",
            name="packetInfo",
            field=models.TextField(
                verbose_name="If you send us packets. Please describe here what kind of material you are sending us. Especially write the purpose of the material, i.e., denote whether the material is for your booth or the conference bags. Provide general information here. Please enter your parcels with tracking number below in order to help us to identify and sort incoming packets.",
                blank=True,
            ),
            preserve_default=True,
        ),
    ]
