# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-11 13:44


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sponsor", "0024_sponsoring_displaycompanyname"),
    ]

    operations = [
        migrations.AddField(
            model_name="sponsoring",
            name="year",
            field=models.PositiveIntegerField(
                default=1,
                editable=False,
                verbose_name="Conference year this sponsoring belongs to",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="sponsorpackage",
            name="year",
            field=models.PositiveIntegerField(
                default=1,
                editable=False,
                verbose_name="Conference year this package belongs to",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="sponsorcontact",
            name="contactEMail",
            field=models.EmailField(
                max_length=254, verbose_name="General contact mail"
            ),
        ),
        migrations.AlterField(
            model_name="sponsorcontact",
            name="contactPersonEmail",
            field=models.EmailField(
                blank=True, max_length=254, verbose_name="Contact person email"
            ),
        ),
    ]
