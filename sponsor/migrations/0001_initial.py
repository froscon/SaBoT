# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SponsorContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('companyName', models.CharField(max_length=128, verbose_name='Company name')),
                ('contactEMail', models.EmailField(max_length=75, verbose_name='General contact mail')),
                ('street', models.CharField(max_length=128, verbose_name='Street')),
                ('zipcode', models.CharField(max_length=16, verbose_name='ZIP Code')),
                ('city', models.CharField(max_length=64, verbose_name='City')),
                ('country', models.CharField(max_length=64, verbose_name='Country', blank=True)),
                ('responded', models.BooleanField(default=False, verbose_name='This sponsor did react to our contact attempt')),
                ('contactPersonFirstname', models.CharField(max_length=128, verbose_name='Contact person firstname', blank=True)),
                ('contactPersonSurname', models.CharField(max_length=128, verbose_name='Contact person surname', blank=True)),
                ('contactPersonGender', models.CharField(blank=True, max_length=1, verbose_name='Gender of contact person', choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('contactPersonLanguage', models.CharField(default=b'de-DE', max_length=16, verbose_name='Language of contact person', choices=[(b'de-DE', b'German'), (b'en-US', b'English')])),
                ('contactPersonEmail', models.EmailField(max_length=75, verbose_name='Contact person email', blank=True)),
                ('comment', models.TextField(verbose_name='Comments and Notes', blank=True)),
                ('lastMailed', models.DateField(verbose_name='Last time we mailed this contact', null=True, editable=False, blank=True)),
                ('rtTicketId', models.PositiveIntegerField(verbose_name='RT ticket id', null=True, editable=False, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sponsoring',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modifyDate', models.DateField(auto_now=True)),
                ('adminComment', models.TextField(verbose_name='Internal comments on this sponsor', blank=True)),
                ('rtTicketId', models.PositiveIntegerField(null=True, verbose_name='RT ticket id', blank=True)),
                ('commitment', models.BooleanField(default=False, verbose_name='The sponsor has confirmed the sponsoring')),
                ('logo', models.ImageField(upload_to=b'sponsors/logos', verbose_name='Company logo', blank=True)),
                ('homepage', models.URLField(verbose_name='Company homepage url', blank=True)),
                ('hpTextDE', models.TextField(verbose_name='Description text for our homepage (German)', blank=True)),
                ('hpTextEN', models.TextField(verbose_name='Description text for our homepage (English)', blank=True)),
                ('wantBooth', models.NullBooleanField(verbose_name='Do you want a booth for your company on the conference?')),
                ('boothTables', models.IntegerField(null=True, verbose_name='How many tables do you need for your booth?', blank=True)),
                ('boothChairs', models.IntegerField(null=True, verbose_name=b'How many chairs do you need?', blank=True)),
                ('boothBarTables', models.IntegerField(null=True, verbose_name=b"How many bar tables do you need? Please note that we can only provide tables and don't have bar stools.", blank=True)),
                ('boothComments', models.TextField(verbose_name='Comments, e.g., if you bring your own booth its dimensions', blank=True)),
                ('programAd', models.FileField(upload_to=b'sponsors/ad/', verbose_name='PDF of your advertisement in our printed program', blank=True)),
                ('packetInfo', models.TextField(verbose_name='If you send us packets. Please describe here what kind of material you are sending us. Especially write the purpose of the material, i.e., denote whether the material is for your booth or the conference bags.', blank=True)),
                ('programAdText', models.TextField(verbose_name='Description text.', blank=True)),
                ('wantRecruting', models.NullBooleanField(verbose_name='Do you want to participate in the recruiting event on the conference?')),
                ('twitterAccount', models.CharField(max_length=128, verbose_name=b'Twitter account name', blank=True)),
                ('facebookPage', models.URLField(verbose_name='Facebook fanpage URL', blank=True)),
                ('facebookAccount', models.CharField(max_length=128, verbose_name='Facebook account name', blank=True)),
                ('gplusPage', models.URLField(verbose_name='G+ fanpage URL', blank=True)),
                ('gplusAccount', models.CharField(max_length=128, verbose_name='G+ account name', blank=True)),
                ('contact', models.ForeignKey(related_name='sponsoring', editable=False, to='sponsor.SponsorContact', on_delete=models.CASCADE)),
                ('owner', models.ForeignKey(related_name='sponsorings', editable=False, to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SponsoringParticipants',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('isAdmin', models.BooleanField(default=False)),
                ('project', models.ForeignKey(to='sponsor.Sponsoring', on_delete=models.CASCADE)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SponsorMailAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='Displayed attachment name')),
                ('filepath', models.CharField(max_length=256, verbose_name='Path of the attachment file')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SponsorMailTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('templateName', models.CharField(max_length=128, verbose_name='Template name')),
                ('mailSubject', models.CharField(max_length=256, verbose_name='E-mail subject')),
                ('mailTemplatePath', models.CharField(max_length=128, verbose_name='Mail template filename')),
                ('attachments', models.ManyToManyField(to='sponsor.SponsorMailAttachment', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SponsorPackage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='Package name')),
                ('comments', models.TextField(verbose_name='Comments', blank=True)),
                ('color', models.CharField(default=b'#ffffff', max_length=7, verbose_name='Display color of sponsor package', validators=[django.core.validators.RegexValidator(regex=b'#[0-9a-f]{6}', message='Please enter a HTML color code of format #[0-9a-f]{6}')])),
                ('hasHpText', models.BooleanField(default=False, verbose_name='Has the sponsor texts on our homepage?')),
                ('hasBooth', models.BooleanField(default=False, verbose_name='Has the sponsor the option for a booth on the conference?')),
                ('hasProgramAd', models.BooleanField(default=False, verbose_name='Has the sponsor an advertisement in the printed program?')),
                ('programAdInfo', models.TextField(verbose_name='Displayed information about the size, quality, color, etc on the printed advertisement', blank=True)),
                ('hasPackets', models.BooleanField(default=False, verbose_name='Is the sponsor allowed to send packets to us?')),
                ('hasParticipants', models.BooleanField(default=False, verbose_name='Has the sponsor the option to register VIPs? (usually for booth)')),
                ('hasProgramAdText', models.BooleanField(default=False, verbose_name='Has the sponsor an advertisement text in the printed program?')),
                ('hasRecruitingEvent', models.BooleanField(default=False, verbose_name='Has the sponsor the option to participate in the recruting event?')),
                ('programAdTextNumWords', models.PositiveIntegerField(null=True, verbose_name='How many words is the advertisement text allowed to have?', blank=True)),
                ('numFreeTickets', models.PositiveIntegerField(default=0, verbose_name='How many free tickets gets this sponsor?')),
                ('price', models.DecimalField(verbose_name='Package price', max_digits=32, decimal_places=2)),
                ('countPackages', models.PositiveIntegerField(default=0, verbose_name='How many packages of this type do we sell?')),
                ('invoiceTextDE', models.TextField(verbose_name='Textual description on the invoice (German). Please briefly describe the package contents. The name will be taken from the package name.', blank=True)),
                ('invoiceTextEN', models.TextField(verbose_name='Textual description on the invoice (English) (see german)', blank=True)),
                ('hpCatagoryName', models.CharField(max_length=128, verbose_name='Hompage Catagory')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sponsoring',
            name='package',
            field=models.ForeignKey(related_name='sponsorings', verbose_name='Selected sponsoring package', to='sponsor.SponsorPackage', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sponsoring',
            name='participants',
            field=models.ManyToManyField(related_name='sponsorparticipation', editable=False, to=settings.AUTH_USER_MODEL, through='sponsor.SponsoringParticipants', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sponsorcontact',
            name='template',
            field=models.ForeignKey(verbose_name='Mail contact template', blank=True, to='sponsor.SponsorMailTemplate', null=True, on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
