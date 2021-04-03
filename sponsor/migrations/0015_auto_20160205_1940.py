# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("sponsor", "0014_sponsoring_programadtextoptout"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="sponsorpackage",
            name="invoiceTextDE",
        ),
        migrations.RemoveField(
            model_name="sponsorpackage",
            name="invoiceTextEN",
        ),
        migrations.RemoveField(
            model_name="sponsorpackage",
            name="providesVectorLogo",
        ),
        migrations.AddField(
            model_name="sponsorpackage",
            name="additionalContentTextDE",
            field=models.TextField(
                verbose_name="Additional package contents (german). Additional items that belong to this package but are not automatically generated from the selections above.",
                blank=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="sponsorpackage",
            name="additionalContentTextEN",
            field=models.TextField(
                verbose_name="Additional package contents (English) (see german)",
                blank=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="sponsorpackage",
            name="boothPositionDE",
            field=models.CharField(
                max_length=256,
                verbose_name="Position of booth for packet description (DE)",
                blank=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="sponsorpackage",
            name="boothPositionEN",
            field=models.CharField(
                max_length=256,
                verbose_name="Position of booth for packet description. This text gets printed in the description. Leave empty to just generate an generic item. (EN)",
                blank=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="sponsorpackage",
            name="hasConferenceBagContent",
            field=models.BooleanField(
                default=False,
                verbose_name="Has the sponsor the option to send us contents for the conference bag?",
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="sponsorpackage",
            name="hasLogoOnPrintmedia",
            field=models.BooleanField(
                default=False,
                verbose_name="Is the sponsor's logo is shown on all our printed media?",
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="sponsorpackage",
            name="hasSocialMedia",
            field=models.BooleanField(
                default=True, verbose_name="Has the sponsor social media advertising?"
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="sponsorpackage",
            name="logoWebsitePositionDE",
            field=models.CharField(
                max_length=256,
                verbose_name="Description text for the logo position on our website (German)",
                blank=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="sponsorpackage",
            name="logoWebsitePositionEN",
            field=models.CharField(
                max_length=256,
                verbose_name="Description text for the logo position on our website (English)",
                blank=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="sponsorpackage",
            name="programAdInfoDescDE",
            field=models.CharField(
                max_length=256,
                verbose_name="Information about advertisement in our program for the packet description (DE)",
                blank=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="sponsorpackage",
            name="programAdInfoDescEN",
            field=models.CharField(
                max_length=256,
                verbose_name="Information about advertisement in our program for the packet description (EN)",
                blank=True,
            ),
            preserve_default=True,
        ),
    ]
