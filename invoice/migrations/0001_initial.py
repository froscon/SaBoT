# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("sponsor", "0017_auto_20160207_1118"),
    ]

    operations = [
        migrations.CreateModel(
            name="Invoice",
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
                    "invoiceNumber",
                    models.CharField(
                        unique=True,
                        max_length=64,
                        verbose_name="invoice number",
                        db_index=True,
                    ),
                ),
                (
                    "invoiceAmount",
                    models.PositiveIntegerField(verbose_name="invoice amount"),
                ),
                ("dueDate", models.DateField(verbose_name="Due date")),
                (
                    "pdf",
                    models.FileField(
                        upload_to=b"skinvoices",
                        null=True,
                        verbose_name="invoice pdf",
                        blank=True,
                    ),
                ),
                (
                    "rtTicketRef",
                    models.PositiveIntegerField(
                        null=True,
                        verbose_name="RT Ticket reference for sending this invoice",
                        blank=True,
                    ),
                ),
                (
                    "sponsoring",
                    models.OneToOneField(
                        related_name="invoice",
                        verbose_name="Sponsoring package belonging to this invoice",
                        to="sponsor.Sponsoring",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="InvoiceTemplate",
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
                    "description",
                    models.CharField(
                        max_length=128,
                        verbose_name="Description for the invoice template",
                    ),
                ),
                (
                    "template",
                    models.FileField(
                        upload_to=b"invoice_templates",
                        null=True,
                        verbose_name="Invoice template file",
                        blank=True,
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="SMSKaufenSnailMailJob",
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
                    "jobid",
                    models.PositiveIntegerField(
                        verbose_name="SMSKaufen job identifier"
                    ),
                ),
                (
                    "joberror",
                    models.CharField(
                        max_length=256,
                        verbose_name="Error description of a potential processing error",
                        blank=True,
                    ),
                ),
                (
                    "success",
                    models.BooleanField(
                        default=False, verbose_name="The mail was successfully sent."
                    ),
                ),
                (
                    "sponsoring",
                    models.OneToOneField(
                        related_name="snailmailinvoice",
                        verbose_name="Sponsoring package belonging to this snail mailing job",
                        to="sponsor.Sponsoring",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="invoice",
            name="template",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.SET_NULL,
                verbose_name="Template to use for this invoice",
                to="invoice.InvoiceTemplate",
                null=True,
            ),
            preserve_default=True,
        ),
    ]
