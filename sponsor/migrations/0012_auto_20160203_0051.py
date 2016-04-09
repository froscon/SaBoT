# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0011_auto_20160202_2338'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsoring',
            name='facebookAccountOptOut',
            field=models.BooleanField(default=False, verbose_name='Sponsor does not use a Facebook account'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sponsoring',
            name='facebookPaceOptOut',
            field=models.BooleanField(default=False, verbose_name='Sponsor does not use Facebook fanpage URL'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sponsoring',
            name='gplusAccountOptOut',
            field=models.BooleanField(default=False, verbose_name='Sponsor does not use a G+ account name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sponsoring',
            name='gplusPageOptOut',
            field=models.BooleanField(default=False, verbose_name='Sponsor does not use G+ fanpage URL'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sponsoring',
            name='twitterAccountOptOut',
            field=models.BooleanField(default=False, verbose_name='Sponsor does not use a Twitter account'),
            preserve_default=True,
        ),
    ]
