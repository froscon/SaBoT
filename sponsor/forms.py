# coding: utf8

from crispy_forms.bootstrap import (
    FormActions,
    TabHolder,
    Tab,
    AppendedText,
)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from main.models import ConferenceYear
from sabot.crispy_ext import TextOptOut
from sponsor.models import Sponsoring, SponsorContact, SponsorPackage


class LinkOnlyTab(Tab):
    link_template = "sponsor/participantsLink.html"

    def __init__(self, *args, **kwargs):
        super(LinkOnlyTab, self).__init__(*args, **kwargs)
        self.targ_url = kwargs["targ_url"]

    def render_link(self, template_pack="bootstrap3", **kwargs):
        return render_to_string(self.link_template, {"link": self})


class SponsorMailSelectorForm(forms.Form):
    recipients = forms.ModelMultipleChoiceField(
        queryset=SponsorContact.objects.all(), label=_("Mail recipients")
    )


class PackagesImporterForm(forms.Form):
    fromYear = forms.ModelChoiceField(
        queryset=ConferenceYear.objects.all(), label=_("Import all packages from year")
    )

    def __init__(self, *args, **kwargs):
        super(PackagesImporterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-lg-5"
        self.helper.field_class = "col-lg-5"
        self.helper.layout = Layout(
            Field("fromYear"),
        )
        self.helper.form_action = "sponsorpackage_import"
        self.helper.add_input(Submit("Import", "Import"))


class SponsorContactForm(forms.ModelForm):
    class Meta:
        fields = [
            "responded",
            "companyName",
            "contactEMail",
            "extraContactEmails",
            "street",
            "zipcode",
            "city",
            "country",
            "contactPersonFirstname",
            "contactPersonSurname",
            "contactPersonGender",
            "contactPersonEmail",
            "contactPersonLanguage",
            "template",
            "comment",
        ]
        model = SponsorContact

    def __init__(self, *args, **kwargs):
        super(SponsorContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("responded"),
            Field("companyName"),
            Field("contactEMail"),
            HTML(
                '<p class="text-info">Please ensure the correctness of the address. It will later be used in the billing process.</p>'
            ),
            Field("extraContactEmails"),
            Field("street"),
            Field("zipcode"),
            Field("city"),
            Field("country"),
            Field("contactPersonFirstname"),
            Field("contactPersonSurname"),
            Field("contactPersonGender"),
            Field("contactPersonEmail"),
            Field("contactPersonLanguage"),
            Field("template"),
            Field("comment"),
        )
        self.helper.add_input(Submit("Save", "Save"))


class SponsorContactSelfEditForm(forms.ModelForm):
    class Meta:
        fields = [
            "companyName",
            "contactEMail",
            "street",
            "zipcode",
            "city",
            "country",
            "contactPersonFirstname",
            "contactPersonSurname",
            "contactPersonGender",
            "contactPersonEmail",
            "contactPersonLanguage",
        ]
        model = SponsorContact

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("companyName"),
            Field("contactEMail"),
            Field("street"),
            Field("zipcode"),
            Field("city"),
            Field("country"),
            Field("contactPersonFirstname"),
            Field("contactPersonSurname"),
            Field("contactPersonGender"),
            Field("contactPersonEmail"),
            Field("contactPersonLanguage"),
        )
        self.helper.add_input(Submit("Save", "Save"))


class SponsorCreationForm(forms.Form):
    sponsorContact = forms.ModelChoiceField(
        queryset=SponsorContact.objects.all(), label=_("Sponsor Contact")
    )
    sponsorUsername = forms.RegexField(
        regex=r"^[\w.@+-]+$",
        max_length=30,
        label=_("Username for new sponsor account"),
        error_messages={
            "invalid": _(
                "This value may contain only letters, numbers and @/./+/-/_ characters."
            )
        },
    )
    sponsorPackage = forms.ModelChoiceField(
        queryset=SponsorPackage.objects.all(), label=_("Select sponsoring package")
    )
    internalComment = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label=_("Internal comments on this sponsor"),
    )

    def __init__(self, *args, **kwargs):
        year = kwargs.pop("year")
        super(SponsorCreationForm, self).__init__(*args, **kwargs)
        self.fields["sponsorPackage"].queryset = SponsorPackage.objects.filter(year=year)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field("sponsorUsername"), Field("sponsorPackage"), Field("internalComment")
        )
        self.helper.add_input(Submit("Save", "Create sponsor"))

    def clean_sponsorContact(self):
        sponsorContact = self.cleaned_data["sponsorContact"]
        if sponsorContact is not None:
            if (
                sponsorContact.contactPersonEmail is None
                or len(sponsorContact.contactPersonEmail) == 0
            ):
                raise ValidationError(
                    "You have to use a company contact with personal contact. Please check the sponsoring contact entry you used."
                )
        return sponsorContact


class SponsorPackageForm(forms.ModelForm):
    class Meta:
        model = SponsorPackage
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(SponsorPackageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("name"),
            Field("hpCatagoryName"),
            Field("comments"),
            Field("color"),
            AppendedText("price", "€"),
            Field("countPackages"),
            Field("logoWebsitePositionEN"),
            Field("logoWebsitePositionDE"),
            Field("hasLogoOnPrintmedia"),
            Field("hasSocialMedia"),
            Field("hasHpText"),
            Field("hasProgramAdText"),
            Field("programAdTextNumWords"),
            Field("hasProgramAd"),
            Div(
                Field("programAdInfo"),
                Field("programAdInfoDescEN"),
                Field("programAdInfoDescDE"),
                HTML('<div class="form-grouper-label">Program ad</div>'),
                css_class="form-grouper",
                css_id="program-ad-grouper",
            ),
            Field("hasPackets"),
            Field("hasBooth"),
            Div(
                Field("boothPositionEN"),
                Field("boothPositionDE"),
                HTML('<div class="form-grouper-label">Booth position</div>'),
                css_class="form-grouper",
                css_id="booth-grouper",
            ),
            Field("hasRecruitingEvent"),
            Field("hasParticipants"),
            Field("numFreeTickets"),
            Field("additionalContentTextEN"),
            Field("additionalContentTextDE"),
        )
        self.helper.add_input(Submit("Save", "Save"))


class SponsorForm(forms.ModelForm):
    class Meta:
        exclude = ()
        model = Sponsoring

        widgets = {
            "logo": forms.widgets.FileInput,
        }

    def __init__(self, *args, **kwargs):
        adminForm = False
        if "request" in kwargs and kwargs["request"].user is not None:
            adminForm = kwargs["request"].user.is_staff
            del kwargs["request"]

        super(SponsorForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        instance = kwargs.get("instance", None)
        if instance is None:
            raise ValueError("Instance has to be set to use this form")

        tablist = []

        if not adminForm:
            del self.fields["package"]
            del self.fields["adminComment"]
            del self.fields["commitment"]
            del self.fields["rtTicketId"]
            del self.fields["clearedForBilling"]
            del self.fields["socialMediaAnnounced"]

        if adminForm:
            adminList = [
                Div(
                    HTML(
                        "<strong>Connected with <a href=\"{% url 'sponsorcontact_update' pk=object.contact.pk %}\">{{object.contact.companyName}}</a></strong>"
                    ),
                    css_class="form-group",
                ),
                Field("package"),
                Field("commitment"),
                Field("clearedForBilling"),
                Field("rtTicketId"),
            ]
            if instance.package.hasSocialMedia:
                adminList.append(Field("socialMediaAnnounced"))

            adminList.extend(
                [
                    Field("adminComment"),
                    Div(
                        HTML(
                            '<p>The access link for the sponsor is <a href="'
                            + settings.SPONSOR_URL
                            + "{% url 'auth_token' token=object.owner.legacy_profile.authToken %}\">"
                            + settings.SPONSOR_URL
                            + "{% url 'auth_token' token=object.owner.legacy_profile.authToken %}</a></p>"
                        ),
                        css_class="form-group",
                    ),
                ]
            )

            tablist.append(Tab("Admin", *adminList))

        general_fields = [Field("displayCompanyName"), Field("logo")]
        if instance.logo:
            general_fields.append(
                Div(
                    HTML(
                        '<p>Current logo:</p><img src="{{object.logo.url}}" style="max-height:200px"/>'
                    ),
                    css_class="control-group",
                )
            )

        if instance.package.hasLogoOnPrintmedia:
            general_fields.append(Field("vectorLogo"))

        textOptOutNotice = Div(
            HTML(
                'Please use the <span class="glyphicon glyphicon-ban-circle"></span>-button in fields to indicate that you will not fill the respective field.'
            ),
            css_class="alert alert-info",
        )

        general_fields.append(Field("homepage"))
        tablist.append(Tab("General", *general_fields))
        contact = instance.contact
        contact_info = render_to_string('sponsor/sponsoring/contactinfo.html', {'contact': contact})
        tablist.append(
            Tab(
                "Contact Info",
                HTML(contact_info)
            )
        )
        tablist.append(
            Tab(
                "Billing Address",
                textOptOutNotice,
                TextOptOut("billingReference"),
                Field("billingAddress"),
                Field("billingInForeignCountry"),
            )
        )
        if instance.package.hasSocialMedia:
            tablist.append(
                Tab(
                    "Social Media",
                    textOptOutNotice,
                    TextOptOut("twitterAccount"),
                    TextOptOut("facebookAccount"),
                    TextOptOut("facebookPage"),
                    TextOptOut("linkedinPage"),
                )
            )
        if instance.package.hasHpText:
            tablist.append(
                Tab("Conference Homepage", Field("hpTextDE"), Field("hpTextEN"))
            )
        if instance.package.hasBooth:
            tablist.append(
                Tab(
                    "Booth",
                    Field("wantBooth"),
                    Field("boothTables"),
                    Field("boothChairs"),
                    Field("boothBarTables"),
                    Field("boothComments"),
                )
            )
        if instance.package.hasRecruitingEvent:
            tablist.append(
                Tab(
                    "Recruiting",
                    Field("wantRecruting"),
                    Field("recruitingInfoDE"),
                    Field("recruitingInfoEN"),
                )
            )
        if instance.package.hasPackets:
            tablist.append(
                Tab(
                    "Parcel",
                    Field("packetInfo"),
                    HTML(
                        '<p class="text-info">We will prepare approximately <strong>{} conference bags</strong>. If you send us less bag inserts, please briefly explain the way in which we should distribute your bag inserts.</p>\n<p class="text-info">Please assure that no packets arrive before {} and use the following address to send us packets:</p>{{{{object.contact.companyName}}}}<br />c/o {}\n<br /><br />'.format(
                            settings.NUMBER_OF_CONFERENCE_BAGS,
                            settings.PACKETS_DELIVERY_START.strftime("%a %b %d %Y"),
                            settings.CONFERENCE_VENUE_ADDRESS.replace("\n", "<br />"),
                        )
                    ),
                    HTML(
                        '<p class="text-info">Please enter your parcel in the <a href="{}"><span class="glyphicon glyphicon-list"></span> <strong>tracking manager</strong></a> once you sent them to simplify our work and track whether we received your parcel.</p>'.format(
                            reverse(
                                "sponsor_parcel_tracking", kwargs={"lpk": instance.pk}
                            )
                        ),
                    ),
                )
            )
        if instance.package.hasProgramAd and instance.package.hasProgramAdText:
            tablist.append(
                Tab(
                    "Printed program",
                    textOptOutNotice,
                    HTML(
                        '<p class="text-info">Please consider the following information regarding your advertisement in out printed program:<br />{{object.package.programAdInfo}}</p>'
                    ),
                    Field("programAd"),
                    HTML(
                        '<p class="text-info">Additionally, you can enter a short description text of <strong>{{object.package.programAdTextNumWords}} words</strong> to describe your company.'
                    ),
                    TextOptOut("programAdText"),
                )
            )
        elif instance.package.hasProgramAd:
            tablist.append(
                Tab(
                    "Printed program",
                    HTML(
                        '<p class="text-info">Please consider the following information regarding your advertisement in out printed program:<br />{{object.package.programAdInfo}}</p>'
                    ),
                    Field("programAd"),
                )
            )
        elif instance.package.hasProgramAdText:
            tablist.append(
                Tab(
                    "Printed program",
                    textOptOutNotice,
                    HTML(
                        '<p class="text-info">You can provide a short description text of <strong>{{object.package.programAdTextNumWords}} words</strong> to describe your company.'
                    ),
                    TextOptOut("programAdText"),
                ),
            )
        if instance.package.hasParticipants:
            tablist.append(
                Tab(
                    "Participants",
                    HTML(
                        '<p class="text-info">Partipants can be added/removed and listed in the <a href="{}"><span class="glyphicon glyphicon-list"></span> <strong>Partipants manager</strong></a>'.format(
                            reverse("sponsor_participants", kwargs={"pk": instance.pk})
                        )
                    ),
                )
            )

        actions = FormActions(Submit("Save", "Save changes"))

        self.helper.layout = Layout(TabHolder(*tablist), actions)

    def clean_programAdText(self):
        text = self.cleaned_data["programAdText"]
        words = len(text.split())
        if (
            self.instance.package.hasProgramAdText
            and words > self.instance.package.programAdTextNumWords
        ):
            raise forms.ValidationError(
                "Your text is too long. It has {0} words but only {1} are allowed.".format(
                    words, self.instance.package.programAdTextNumWords
                )
            )
        return text

    def clean_clearedForBilling(self):
        cfb = self.cleaned_data["clearedForBilling"]
        if cfb and self.instance is not None:
            if self.instance.billingAddressStatus() != 2:
                raise forms.ValidationError(
                    "This sponsoring has an incomplete billing address. Hence, you cannot clear it for billing."
                )
        return cfb

    def clean(self):
        cleaned_data = super(SponsorForm, self).clean()
        if (
            ("boothTables" in cleaned_data and cleaned_data["boothTables"] is not None)
            or (
                "boothBarTables" in cleaned_data
                and cleaned_data["boothBarTables"] is not None
            )
            or ("boothComments" in cleaned_data and cleaned_data["boothComments"] != "")
        ) and ("wantBooth" not in cleaned_data or not cleaned_data["wantBooth"]):
            self._errors["wantBooth"] = self.error_class(
                ["You must indicate that you want a booth at all"]
            )
        return cleaned_data
