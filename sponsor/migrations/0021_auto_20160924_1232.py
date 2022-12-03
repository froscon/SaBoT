# -*- coding: utf-8 -*-


from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("sponsor", "0020_sponsoring_socialmediaannounced"),
    ]

    operations = [
        migrations.CreateModel(
            name="SponsorMail",
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
                    "mailTemplateName",
                    models.CharField(max_length=128, verbose_name="Mail template name"),
                ),
                (
                    "mailSubject",
                    models.CharField(max_length=256, verbose_name="E-mail subject"),
                ),
                (
                    "attachments",
                    models.ManyToManyField(
                        to="sponsor.SponsorMailAttachment", blank=True
                    ),
                ),
                (
                    "template",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.SET_NULL,
                        verbose_name="Mail text template",
                        to="sponsor.SponsorMailTemplate",
                        null=True,
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name="sponsormailtemplate",
            name="attachments",
        ),
        migrations.RemoveField(
            model_name="sponsormailtemplate",
            name="mailSubject",
        ),
        migrations.RemoveField(
            model_name="sponsormailtemplate",
            name="mailTemplatePath",
        ),
        migrations.AddField(
            model_name="sponsormailtemplate",
            name="template",
            field=models.TextField(default="", verbose_name="Django template content"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="sponsormailattachment",
            name="name",
            field=models.CharField(
                max_length=128, verbose_name="Displayed attachment file name"
            ),
            preserve_default=True,
        ),
    ]
