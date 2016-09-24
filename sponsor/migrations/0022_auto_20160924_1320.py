# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0021_auto_20160924_1232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sponsormailattachment',
            name='filepath',
        ),
        migrations.AddField(
            model_name='sponsormailattachment',
            name='attachment',
            field=models.FileField(default=None, upload_to=b'sponsormail_attachments', verbose_name='The contact mail attachment'),
            preserve_default=False,
        ),
    ]
