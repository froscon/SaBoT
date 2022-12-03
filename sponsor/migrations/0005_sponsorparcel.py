# -*- coding: utf-8 -*-


from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("sponsor", "0004_auto_20150619_2212"),
    ]

    operations = [
        migrations.CreateModel(
            name="SponsorParcel",
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
                        verbose_name="Tracking URL (if available", blank=True
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
                    models.BooleanField(default=False, verbose_name="Received"),
                ),
                (
                    "storageLocation",
                    models.TextField(verbose_name="Storage location", blank=True),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        related_name="parcels",
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "sponsoring",
                    models.ForeignKey(
                        related_name="parcels",
                        editable=False,
                        to="sponsor.Sponsoring",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
    ]
