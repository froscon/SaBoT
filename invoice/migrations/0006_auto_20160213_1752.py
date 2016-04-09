# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0005_auto_20160208_2036'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=128, verbose_name='Description for the invoice template')),
                ('template', models.FileField(upload_to=b'invoice_templates', null=True, verbose_name='Invoice template file (odt)', blank=True)),
                ('docType', models.CharField(max_length=16, verbose_name='Type of this document template', choices=[(b'INVOICE', 'Invoice template'), (b'OFFER', 'Offer template')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Template to use for this invoice', to='invoice.DocumentTemplate', null=True),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='InvoiceTemplate',
        ),
    ]
