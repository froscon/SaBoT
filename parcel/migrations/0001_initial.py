# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Parcel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "ownerId",
                    models.PositiveIntegerField(
                        verbose_name="Key of the owner object",
                        null=True,
                        editable=False,
                        blank=True,
                    ),
                ),
                (
                    "createDate",
                    models.DateField(auto_now_add=True, verbose_name="Creation date"),
                ),
                (
                    "parcelService",
                    models.CharField(
                        max_length=128, verbose_name="Delivery service company"
                    ),
                ),
                (
                    "trackingNumber",
                    models.CharField(max_length=128, verbose_name="Tracking number"),
                ),
                (
                    "trackingUrl",
                    models.URLField(
                        verbose_name="Tracking URL (if available)", blank=True
                    ),
                ),
                (
                    "contentAndUsage",
                    models.TextField(
                        verbose_name="What is the content of this package? What should we use it for?",
                        blank=True,
                    ),
                ),
                (
                    "received",
                    models.BooleanField(
                        default=False,
                        verbose_name="We received this package (tick this and enter storage location once handled)",
                    ),
                ),
                (
                    "storageLocation",
                    models.TextField(verbose_name="Storage location", blank=True),
                ),
                (
                    "ownerType",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        to="contenttypes.ContentType",
                        null=True,
                        verbose_name="Type of the owner object",
                        on_delete=models.SET_NULL,
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
    ]
