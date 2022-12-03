# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("sponsor", "0022_auto_20160924_1320"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sponsorcontact",
            name="template",
            field=models.ForeignKey(
                verbose_name="Mail contact template",
                blank=True,
                to="sponsor.SponsorMail",
                null=True,
                on_delete=models.CASCADE,
            ),
            preserve_default=True,
        ),
    ]
