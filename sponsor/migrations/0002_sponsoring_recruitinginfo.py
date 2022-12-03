# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("sponsor", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="sponsoring",
            name="recruitingInfo",
            field=models.TextField(
                verbose_name="What are you looking for? Only short job descriptions. Internships? Bachelor's/Master's thesis?",
                blank=True,
            ),
            preserve_default=True,
        ),
    ]
