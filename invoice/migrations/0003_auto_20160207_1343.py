# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0002_auto_20160207_1240'),
    ]

    operations = [
        migrations.CreateModel(
            name='YearlyInvoiceCounters',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.PositiveIntegerField(verbose_name='The year this counter belongs to')),
                ('counter', models.PositiveIntegerField(verbose_name='The current counter value')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='invoice',
            name='creationDate',
            field=models.DateField(default=datetime.date(2016, 2, 7), verbose_name='Creation date', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoiceAmount',
            field=models.PositiveIntegerField(verbose_name='Invoice amount', editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoiceNumber',
            field=models.CharField(unique=True, max_length=64, verbose_name='Invoice number', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='payed',
            field=models.BooleanField(default=False, verbose_name='This invoice is payed.', editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='pdf',
            field=models.FileField(verbose_name='Invoice pdf', upload_to=b'skinvoices', null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='rtTicketRef',
            field=models.PositiveIntegerField(verbose_name='RT Ticket reference for sending this invoice', null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='sponsoring',
            field=models.OneToOneField(related_name='invoice', editable=False, to='sponsor.Sponsoring', verbose_name='Sponsoring package belonging to this invoice', on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
