# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-16 13:51


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sponsor", "0025_auto_20170111_1444"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sponsorpackage",
            name="hasLogoOnPrintmedia",
            field=models.BooleanField(
                default=False,
                verbose_name="Is the sponsor's logo shown on all our printed media?",
            ),
        ),
        migrations.AlterField(
            model_name="sponsorpackage",
            name="hpCatagoryName",
            field=models.CharField(max_length=128, verbose_name="Homepage Catagory"),
        ),
    ]
