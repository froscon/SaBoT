# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("sponsor", "0017_auto_20160207_1118"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="sponsoring",
            name="billingAddress2",
        ),
        migrations.RemoveField(
            model_name="sponsoring",
            name="billingCity",
        ),
        migrations.RemoveField(
            model_name="sponsoring",
            name="billingCountry",
        ),
        migrations.RemoveField(
            model_name="sponsoring",
            name="billingName",
        ),
        migrations.RemoveField(
            model_name="sponsoring",
            name="billingStreet",
        ),
        migrations.RemoveField(
            model_name="sponsoring",
            name="billingZipcode",
        ),
        migrations.AddField(
            model_name="sponsoring",
            name="billingAddress",
            field=models.TextField(verbose_name="Your billing address", blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="sponsoring",
            name="billingInForeignCountry",
            field=models.BooleanField(
                default=False, verbose_name="The address above is not in Germany"
            ),
            preserve_default=True,
        ),
    ]
