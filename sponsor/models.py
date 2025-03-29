# -*- coding: utf-8 -*-

import datetime
from decimal import Decimal, localcontext, ROUND_HALF_EVEN
import re
import os.path

from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from sabot.utils import random_filename_generator


class SponsorMailAttachment(models.Model):
    name = models.CharField(
        max_length=128, verbose_name=_("Displayed attachment file name")
    )
    attachment = models.FileField(
        upload_to="sponsormail_attachments",
        verbose_name=_("The contact mail attachment"),
    )

    def __str__(self):
        return self.name


class SponsorMailTemplate(models.Model):
    templateName = models.CharField(max_length=128, verbose_name=_("Template name"))
    template = models.TextField(verbose_name=_("Django template content"))

    def __str__(self):
        return self.templateName


class SponsorMail(models.Model):
    mailTemplateName = models.CharField(
        max_length=128, verbose_name=_("Mail template name")
    )
    template = models.ForeignKey(
        SponsorMailTemplate,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Mail text template"),
    )
    mailSubject = models.CharField(max_length=256, verbose_name=_("E-mail subject"))
    attachments = models.ManyToManyField(SponsorMailAttachment, blank=True)

    def __str__(self):
        return self.mailTemplateName


class SponsorContact(models.Model):
    class Meta:
        ordering = ["companyName"]

    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
        ("D", "Diverse"),
    )
    LANGUAGE_CHOICES = (
        ("de-DE", "German"),
        ("en-US", "English"),
    )
    companyName = models.CharField(max_length=128, verbose_name=_("Company name"))
    contactEMail = models.EmailField(verbose_name=_("General contact mail"))
    address2 = models.CharField(
        blank=True, max_length=128, verbose_name=_("Address addition")
    )
    street = models.CharField(max_length=128, verbose_name=_("Street"))
    zipcode = models.CharField(
        max_length=16, verbose_name=_("ZIP Code")
    )  # this is a char field to stay flexible for foreign addresses
    city = models.CharField(max_length=64, verbose_name=_("City"))
    country = models.CharField(blank=True, max_length=64, verbose_name=_("Country"))
    responded = models.BooleanField(
        verbose_name=_("This sponsor did react to our contact attempt"), default=False
    )
    contactPersonFirstname = models.CharField(
        blank=True, max_length=128, verbose_name=_("Contact person firstname")
    )
    contactPersonSurname = models.CharField(
        blank=True, max_length=128, verbose_name=_("Contact person surname")
    )
    contactPersonGender = models.CharField(
        max_length=1,
        blank=True,
        choices=GENDER_CHOICES,
        verbose_name=_("Gender of contact person"),
    )
    contactPersonLanguage = models.CharField(
        max_length=16,
        choices=LANGUAGE_CHOICES,
        verbose_name=_("Language of contact person"),
        default="de-DE",
    )
    contactPersonEmail = models.EmailField(
        blank=True, verbose_name=_("Contact person email")
    )
    extraContactEmails = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=_("Further contact mails"),
        help_text=_("An empty or comma separated list of additional contact mails"),
        validators=[RegexValidator("^([^@,]+@[^@,]+\\.[^@,]+)(,[^@,]+@[^@,]+\\.[^@,]+)*$",
                                   "Not valid comma separated mails list.")]
    )

    comment = models.TextField(blank=True, verbose_name=_("Comments and Notes"))
    template = models.ForeignKey(
        SponsorMail,
        blank=True,
        null=True,
        verbose_name=_("Mail contact template"),
        on_delete=models.SET_NULL,
    )

    lastMailed = models.DateField(
        blank=True,
        null=True,
        editable=False,
        verbose_name=_("Last time we mailed this contact"),
    )
    rtTicketId = models.PositiveIntegerField(
        blank=True, null=True, editable=False, verbose_name=_("RT ticket id")
    )

    def allDataAvailable(self):
        return (
            self.companyName != ""
            and self.contactPersonEmail != ""
            and self.street != ""
            and self.zipcode != ""
            and self.zipcode != "0"
            and self.city != ""
            and self.contactPersonFirstname != ""
            and self.contactPersonSurname != ""
            and self.contactPersonEmail != ""
            and self.template is not None
        )

    def wasRecentlyMailed(self):
        if self.lastMailed == None:
            return False
        timedelta = datetime.date.today() - self.lastMailed
        if timedelta.days < 31:
            return True
        return False

    def __str__(self):
        return self.companyName


class SponsorPackage(models.Model):
    name = models.CharField(max_length=128, verbose_name=_("Package name"))
    comments = models.TextField(blank=True, verbose_name=_("Comments"))
    color = models.CharField(
        default="#ffffff",
        max_length=7,
        verbose_name=_("Display color of sponsor package"),
        validators=[
            RegexValidator(
                regex=r"#[0-9a-f]{6}",
                message=_("Please enter a HTML color code of format #[0-9a-f]{6}"),
            )
        ],
    )

    # the properties of this package
    logoWebsitePositionDE = models.CharField(
        blank=True,
        max_length=256,
        verbose_name=_(
            "Description text for the logo position on our website (German)"
        ),
    )
    logoWebsitePositionEN = models.CharField(
        blank=True,
        max_length=256,
        verbose_name=_(
            "Description text for the logo position on our website (English)"
        ),
    )
    hasHpText = models.BooleanField(
        default=False, verbose_name=_("Has the sponsor texts on our homepage?")
    )
    hasLogoOnPrintmedia = models.BooleanField(
        default=False,
        verbose_name=_("Is the sponsor's logo shown on all our printed media?"),
    )
    hasSocialMedia = models.BooleanField(
        default=True, verbose_name=_("Has the sponsor social media advertising?")
    )
    hasConferenceBagContent = models.BooleanField(
        default=False,
        verbose_name=_(
            "Has the sponsor the option to send us contents for the conference bag?"
        ),
    )
    hasBooth = models.BooleanField(
        default=False,
        verbose_name=_("Has the sponsor the option for a booth on the conference?"),
    )
    boothPositionEN = models.CharField(
        blank=True,
        max_length=256,
        verbose_name=_(
            "Position of booth for packet description. This text gets printed in the description. Leave empty to just generate an generic item. (EN)"
        ),
    )
    boothPositionDE = models.CharField(
        blank=True,
        max_length=256,
        verbose_name=_("Position of booth for packet description (DE)"),
    )
    hasProgramAd = models.BooleanField(
        default=False,
        verbose_name=_("Has the sponsor an advertisement in the printed program?"),
    )
    programAdInfo = models.TextField(
        blank=True,
        verbose_name=_(
            "Displayed information about the size, quality, color, etc on the printed advertisement"
        ),
    )
    programAdInfoDescEN = models.CharField(
        blank=True,
        max_length=256,
        verbose_name=_(
            "Information about advertisement in our program for the packet description (EN)"
        ),
    )
    programAdInfoDescDE = models.CharField(
        blank=True,
        max_length=256,
        verbose_name=_(
            "Information about advertisement in our program for the packet description (DE)"
        ),
    )
    hasPackets = models.BooleanField(
        default=False, verbose_name=_("Is the sponsor allowed to send packets to us?")
    )
    hasParticipants = models.BooleanField(
        default=False,
        verbose_name=_(
            "Has the sponsor the option to register VIPs? (usually for booth)"
        ),
    )
    hasProgramAdText = models.BooleanField(
        default=False,
        verbose_name=_("Has the sponsor an advertisement text in the printed program?"),
    )
    hasRecruitingEvent = models.BooleanField(
        default=False,
        verbose_name=_(
            "Has the sponsor the option to participate in the recruting event?"
        ),
    )
    programAdTextNumWords = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_("How many words is the advertisement text allowed to have?"),
    )
    numFreeTickets = models.PositiveIntegerField(
        default=0, verbose_name=_("How many free tickets gets this sponsor?")
    )
    price = models.DecimalField(
        max_digits=32, decimal_places=2, verbose_name=_("Package price")
    )
    countPackages = models.PositiveIntegerField(
        default=0, verbose_name=_("How many packages of this type do we sell?")
    )
    additionalContentTextDE = models.TextField(
        blank=True, verbose_name=_("Additional package contents (German). See English")
    )
    additionalContentTextEN = models.TextField(
        blank=True,
        verbose_name=_(
            "Additional package content (English). Additional items that belong to this package but are not automatically generated from the selections above."
        ),
    )
    hpCatagoryName = models.CharField(
        max_length=128, verbose_name=_("Homepage Catagory")
    )

    year = models.PositiveIntegerField(
        editable=False, verbose_name=_("Conference year this package belongs to")
    )

    def getPriceNet(self):
        return self.price.quantize(Decimal("0.01"))

    def getPriceGross(self):
        with localcontext() as ctx:
            ctx.rounding = ROUND_HALF_EVEN

            vatPercent = Decimal(settings.INVOICE_VAT) * Decimal("0.01")
            grossPrice = self.price + (self.price * vatPercent)
            return grossPrice.quantize(Decimal("0.01"))

    def getVATAmount(self):
        with localcontext() as ctx:
            ctx.rounding = ROUND_HALF_EVEN

            vatPercent = Decimal(settings.INVOICE_VAT) * Decimal("0.01")
            vatAmount = self.price * vatPercent
            return vatAmount.quantize(Decimal("0.01"))

    def countSponsorings(self):
        return self.sponsorings.count()

    def countCommitedSponsorings(self):
        return self.sponsorings.filter(commitment=True).count()

    def __str__(self):
        return self.name

    def getPackageDescriptionDE(self):
        return self._getPackageDescription(self.sponsorPackageDescriptionDE)

    def getPackageDescriptionEN(self):
        return self._getPackageDescription(self.sponsorPackageDescriptionEN)

    def _getPackageDescription(self, desc):
        items = []
        # iterate through the description dictionary and append all the results to items
        for k, v in desc:
            if callable(k):
                res = k(self)
            else:
                res = getattr(self, k)
            if res:
                if callable(v):
                    content = v(self)
                    if isinstance(content, (list, tuple)):
                        items.extend(content)
                    else:
                        items.append(content)
                else:
                    items.append(v)
        return items

    sponsorPackageDescriptionDE = [
        (
            "hasBooth",
            lambda s: s.boothPositionDE
            if len(s.boothPositionDE) > 0
            else "Ausstellungsplatz",
        ),
        ("hasRecruitingEvent", "Stand auf der Recruitingsession"),
        ("hasConferenceBagContent", "Informationsmaterial in den Konferenztaschen"),
        (lambda s: True, lambda s: s.logoWebsitePositionDE),
        (
            "hasLogoOnPrintmedia",
            "Logopräsenz auf allen Werbemitteln (z. B. Badges, Besucherflyer, Plakat)",
        ),
        (
            "hasSocialMedia",
            "Namentliche Erwähnung auf unseren SocialMedia Kanälen (Twitter, Facebook, G+)",
        ),
        (
            "hasProgramAd",
            lambda s: "Anzeige im Konferenzprogramm ({})".format(
                s.programAdInfoDescDE
            ),
        ),
        (
            "hasProgramAdText",
            lambda s: "Text im Konferenzprogramm ({} Wörter)".format(
                s.programAdTextNumWords
            ),
        ),
        (
            lambda s: True,
            lambda s: [
                text.strip()
                for text in s.additionalContentTextDE.strip().split("\n")
                if text.strip() != ""
            ],
        ),
    ]
    sponsorPackageDescriptionEN = [
        (
            "hasBooth",
            lambda s: s.boothPositionEN
            if len(s.boothPositionEN) > 0
            else "Exhibition space",
        ),
        ("hasRecruitingEvent", "Booth at the recruiting session"),
        ("hasConferenceBagContent", "Advertising material in the conference bags"),
        (lambda s: True, lambda s: s.logoWebsitePositionEN),
        (
            "hasLogoOnPrintmedia",
            "Your logo on all publications (e. g. flyers, posters, badges)",
        ),
        (
            "hasSocialMedia",
            "Official mention of sponsorship on our social media channels (Twitter, Facebook, G+)",
        ),
        (
            "hasProgramAd",
            lambda s: "Advertisement in the printed conference program ({})".format(
                s.programAdInfoDescEN
            ),
        ),
        (
            "hasProgramAdText",
            lambda s: "Text in the printed conference program ({} words)".format(
                s.programAdTextNumWords
            ),
        ),
        (
            lambda s: True,
            lambda s: [
                text.strip()
                for text in s.additionalContentTextEN.strip().split("\n")
                if text.strip() != ""
            ],
        ),
    ]

    def toJSON(self):
        return {
            "name": self.name,
            "hasHpText": self.hasHpText,
            "hasBooth": self.hasBooth,
            "hasProgramAd": self.hasProgramAd,
            "hasRecruitingEvent": self.hasRecruitingEvent,
            "price": self.price,
        }


STATUS_COMPLETE = 2
STATUS_MISSING = 0
STATUS_INCOMPLETE = 1
STATUS_NOTINPACKAGE = -1
STATUS_NOTWANTED = -2


def random_filename_upload_logos(instance, filename):
    fn, ext = os.path.splitext(filename)
    while True:
        newname = random_filename_generator() + ext
        path = os.path.join("sponsors/logos", newname)
        if not (settings.MEDIA_ROOT / path).is_file():
            break
    return path


def random_filename_upload_vec_logos(instance, filename):
    fn, ext = os.path.splitext(filename)
    while True:
        newname = random_filename_generator() + ext
        path = os.path.join("sponsors/vec_logos", newname)
        if not (settings.MEDIA_ROOT / path).is_file():
            break
    return path


def random_filename_upload_ad(instance, filename):
    fn, ext = os.path.splitext(filename)
    while True:
        newname = random_filename_generator() + ext
        path = os.path.join("sponsors/ad", newname)
        if not (settings.MEDIA_ROOT / path).is_file():
            break
    return path


class Sponsoring(models.Model):
    class Meta:
        ordering = ["contact"]

    owner = models.ForeignKey(
        User, editable=False, related_name="sponsorings", on_delete=models.CASCADE
    )
    modifyDate = models.DateField(auto_now=True, editable=False)
    contact = models.ForeignKey(
        SponsorContact,
        editable=False,
        related_name="sponsoring",
        on_delete=models.CASCADE,
    )
    package = models.ForeignKey(
        SponsorPackage,
        verbose_name=_("Selected sponsoring package"),
        related_name="sponsorings",
        on_delete=models.CASCADE,
    )
    adminComment = models.TextField(
        blank=True, verbose_name=_("Internal comments on this sponsor")
    )
    rtTicketId = models.PositiveIntegerField(
        blank=True, null=True, verbose_name=_("RT ticket id")
    )
    commitment = models.BooleanField(
        verbose_name=_("The sponsor has confirmed the sponsoring"), default=False
    )

    displayCompanyName = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=_(
            "Company or product name that we should you to announce and advertise your sponsoring"
        ),
    )
    logo = models.ImageField(
        blank=True,
        upload_to=random_filename_upload_logos,
        verbose_name=_("Company logo for homepage (preferably as PNG)"),
    )
    vectorLogo = models.FileField(
        blank=True,
        upload_to=random_filename_upload_vec_logos,
        verbose_name=_(
            "Company logo as vector graphics (preferably PDF or SVG) for printed advertisements such as posters, flyers and visitor badges"
        ),
    )
    homepage = models.URLField(blank=True, verbose_name=_("Company homepage url"))

    hpTextDE = models.TextField(
        blank=True, verbose_name=_("Description text for our homepage (German)")
    )
    hpTextEN = models.TextField(
        blank=True, verbose_name=_("Description text for our homepage (English)")
    )

    wantBooth = models.BooleanField(
        verbose_name=_("Do you want a booth for your company on the conference?"),
        null=True,
    )
    boothTables = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_("How many tables do you need for your booth?"),
    )
    boothChairs = models.IntegerField(
        blank=True, null=True, verbose_name=("How many chairs do you need?")
    )
    boothBarTables = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=(
            "How many bar tables do you need? Please note that we can only provide tables and don't have bar stools."
        ),
    )
    boothComments = models.TextField(
        blank=True,
        verbose_name=_("Comments, e.g., if you bring your own booth its dimensions"),
    )

    programAd = models.FileField(
        blank=True,
        upload_to=random_filename_upload_ad,
        verbose_name=_("PDF of your advertisement in our printed program"),
    )

    packetInfo = models.TextField(
        blank=True,
        verbose_name=_(
            "If you send us packets. Please describe here what kind of material you are sending us. Especially write the purpose of the material, i.e., denote whether the material is for your booth or the conference bags. Provide general information here. Please enter your parcels with tracking number below in order to help us to identify and sort incoming packets."
        ),
    )

    participants = models.ManyToManyField(
        User,
        blank=True,
        editable=False,
        related_name="sponsorparticipation",
        through="SponsoringParticipants",
    )

    programAdText = models.TextField(blank=True, verbose_name=_("Description text."))
    programAdTextOptOut = models.BooleanField(
        default=False, verbose_name=_("Sponsor does not use program ad text")
    )

    wantRecruting = models.BooleanField(
        verbose_name=_(
            "Do you want to participate in the recruiting event on the conference?"
        ),
        null=True,
    )
    recruitingInfoDE = models.TextField(
        blank=True,
        verbose_name=_(
            "What are you looking for? Only short job descriptions. Internships? Bachelor's/Master's thesis? (German)"
        ),
    )
    recruitingInfoEN = models.TextField(
        blank=True, verbose_name=_("Your recruiting keywords (as above) in English")
    )
    twitterAccount = models.CharField(
        blank=True, max_length=128, verbose_name=("Twitter account name")
    )
    twitterAccountOptOut = models.BooleanField(
        default=False, verbose_name=_("Sponsor does not use a Twitter account")
    )
    facebookPage = models.URLField(blank=True, verbose_name=_("Facebook fanpage URL"))
    facebookPageOptOut = models.BooleanField(
        default=False, verbose_name=_("Sponsor does not use Facebook fanpage URL")
    )
    facebookAccount = models.CharField(
        blank=True, max_length=128, verbose_name=_("Facebook account name")
    )
    facebookAccountOptOut = models.BooleanField(
        default=False, verbose_name=_("Sponsor does not use a Facebook account")
    )
    linkedinPage = models.URLField(blank=True, verbose_name=_("Linkedin page URL"))
    linkedinPageOptOut = models.BooleanField(
        default=False, verbose_name=_("Sponsor does not use linkedin page URL")
    )
    socialMediaAnnounced = models.BooleanField(
        default=False, verbose_name=_("Social media announcements were made")
    )

    billingAddress = models.TextField(
        blank=True, verbose_name=_("Your billing address")
    )
    billingInForeignCountry = models.BooleanField(
        default=False, verbose_name=_("The address above is not in Germany")
    )
    billingReference = models.CharField(
        blank=True, max_length=64, verbose_name=_("Your reference number")
    )
    billingReferenceOptOut = models.BooleanField(
        default=False,
        verbose_name=_("Sponsor does not provide a billing reference number"),
    )

    clearedForBilling = models.BooleanField(
        verbose_name=_("This sponsoring is ready for billing"), default=False
    )

    year = models.PositiveIntegerField(
        editable=False, verbose_name=_("Conference year this sponsoring belongs to")
    )

    fieldDescriptionalNames = {  # this is used by email notification
        "logo": _("Company logo"),
        "package": _("Sponsoring package"),
        "adminComment": _("Internal comment"),
        "hpTextDE": _("Homepage text (german)"),
        "hpTextEN": _("Homepage text (english)"),
        "wantBooth": _("Wants booth"),
        "boothTables": _("Tables at booth"),
        "boothBarTables": _("Bartables at booth"),
        "boothChairs": _("Chairs at booth"),
        "boothComments": _("Comment for booth"),
        "programAd": _("Program advertisement"),
        "packetInfo": _("Info for packets"),
        "programAdText": _("Text for printed program"),
        "wantRecruting": _("Wants recruiting event"),
        "recruitingInfo": _("Recruiting job info"),
        "twitterAccount": _("Twitter account name"),
        "facebookAccount": _("Facebook account name"),
        "facebookPage": _("Facebook fanpage"),
        "linkedinPage": _("Linkedin page"),
        "billingName": _("Billing contact person"),
        "billingStreet": _("Billing address street"),
        "billingAddress2": _("Billing addresss addition"),
        "billingZipcode": _("Billing address zipcode"),
        "billingCity": _("Billing address city"),
        "billingCountry": _("Billing address country"),
        "billingReference": _("Billing reference number"),
    }

    def __str__(self):
        return "{} [{}]".format(self.contact.companyName, self.package.name)

    def has_read_permission(self, user):
        return user == self.owner

    def has_write_permission(self, user):
        return user == self.owner

    def logoStatus(self):
        if self.logo and (self.vectorLogo or not self.package.hasLogoOnPrintmedia):
            return STATUS_COMPLETE
        elif self.logo or self.vectorLogo:
            return STATUS_INCOMPLETE
        else:
            return STATUS_MISSING

    def socialMediaStatus(self):
        if not self.package.hasSocialMedia:
            return STATUS_NOTINPACKAGE
        socialMediaItems = [
            self.twitterAccount != "" or self.twitterAccountOptOut,
            self.facebookPage != "" or self.facebookPageOptOut,
            self.facebookAccount != "" or self.facebookPageOptOut,
            self.linkedinPage != "" or self.linkedinPageOptOut,
        ]

        if all(socialMediaItems):
            return STATUS_COMPLETE
        elif any(socialMediaItems):
            return STATUS_INCOMPLETE
        else:
            return STATUS_MISSING

    def billingAddressStatus(self):
        billingAddressItems = [
            self.billingReference != "" or self.billingReferenceOptOut,
            self.billingAddress != "",
        ]

        if all(billingAddressItems):
            return STATUS_COMPLETE
        elif any(billingAddressItems):
            return STATUS_INCOMPLETE
        else:
            return STATUS_MISSING

    def hpLinkStatus(self):
        if self.homepage:
            return STATUS_COMPLETE
        else:
            return STATUS_MISSING

    def hpTextStatus(self):
        if not self.package.hasHpText:
            return STATUS_NOTINPACKAGE
        if self.hpTextDE != "" and self.hpTextEN != "":
            return STATUS_COMPLETE
        elif self.hpTextDE != "" or self.hpTextEN != "":
            return STATUS_INCOMPLETE
        elif self.wantBooth == False:
            return STATUS_NOTWANTED
        else:
            return STATUS_MISSING

    def boothStatus(self):
        if not self.package.hasBooth:
            return STATUS_NOTINPACKAGE
        if self.wantBooth is None:
            return STATUS_MISSING
        if self.wantBooth == False:
            return STATUS_NOTWANTED
        if (
            self.boothTables is not None
            and self.boothChairs is not None
            and self.boothBarTables is not None
        ):
            return STATUS_COMPLETE
        else:
            return STATUS_INCOMPLETE

    def packetsStatus(self):
        if not self.package.hasPackets:
            return STATUS_NOTINPACKAGE
        if self.packetInfo != "":
            return STATUS_COMPLETE
        else:
            return STATUS_NOTWANTED  # its ok to send us no packets

    def programAdStatus(self):
        if not self.package.hasProgramAd:
            return STATUS_NOTINPACKAGE
        if self.programAd:
            return STATUS_COMPLETE
        else:
            return STATUS_NOTINPACKAGE

    def programAdTextStatus(self):
        if not self.package.hasProgramAdText:
            return STATUS_NOTINPACKAGE
        if self.programAdText != "":
            return STATUS_COMPLETE
        elif self.programAdTextOptOut:
            return STATUS_NOTWANTED
        else:
            return STATUS_MISSING

    def participantsStatus(self):
        if not self.package.hasParticipants:
            return STATUS_NOTINPACKAGE
        if len(self.participants.all()) > 0:
            return STATUS_COMPLETE
        elif not (self.wantBooth is None) and self.wantBooth == False:
            return STATUS_NOTWANTED
        else:
            return STATUS_MISSING

    def recruitingStatus(self):
        if not self.package.hasRecruitingEvent:
            return STATUS_NOTINPACKAGE
        elif self.wantRecruting is None:
            return STATUS_MISSING
        elif self.wantRecruting == False:
            return STATUS_NOTWANTED
        elif self.recruitingInfoDE != "" and self.recruitingInfoEN != "":
            return STATUS_COMPLETE
        elif self.recruitingInfoDE != "" or self.recruitingInfoEN != "":
            return STATUS_INCOMPLETE
        else:
            return STATUS_MISSING

    def getBillingAddress(self):
        return self.billingAddress

    def isBillingInForeignCountry(self):
        return self.billingInForeignCountry

    def getPacketDescription(self):
        if self.contact.contactPersonLanguage.startswith("de"):
            return self.package.getPackageDescriptionDE()
        else:
            return self.package.getPackageDescriptionEN()

    def getStatusData(self):
        statusData = []
        for name, link, testF, deadline, statusF in self.inputStatusList:
            if testF(self.package):
                statusData.append(
                    {
                        "name": name,
                        "link": link,
                        "deadline": deadline,
                        "overdue": False
                        if deadline is None
                        else (deadline < datetime.date.today()),
                        "dueWarn": (
                            deadline - settings.DUE_WARNING_TIME < datetime.date.today()
                        )
                        if deadline is not None
                        else False,
                        "status": statusF(self),
                    }
                )

        return statusData

    inputStatusList = [
        # table contents:
        # Description, CorrespondingInputTab, TestFunction (if present), Deadline, Status Function
        (
            "Your website link",
            "#general",
            lambda p: True,
            None,
            lambda s: s.hpLinkStatus,
        ),
        (
            "Logo (website)",
            "#general",
            lambda p: True,
            None,
            lambda s: STATUS_COMPLETE if s.logo else STATUS_MISSING,
        ),
        (
            "Logo (print)",
            "#general",
            lambda p: p.hasLogoOnPrintmedia,
            None,
            lambda s: STATUS_COMPLETE if s.vectorLogo else STATUS_MISSING,
        ),
        (
            "Billing addresss",
            "#billing-address",
            lambda p: True,
            None,
            lambda s: s.billingAddressStatus,
        ),
        (
            "Social media accounts",
            "#social-media",
            lambda p: p.hasSocialMedia,
            None,
            lambda s: s.socialMediaStatus,
        ),
        (
            "Homepage description texts (for exhibitor directory)",
            "#conference-homepage",
            lambda p: p.hasHpText,
            settings.BOOTH_DATA_DEADLINE,
            lambda s: s.hpTextStatus,
        ),
        (
            "Booth",
            "#booth",
            lambda p: p.hasBooth,
            settings.BOOTH_DATA_DEADLINE,
            lambda s: s.boothStatus,
        ),
        (
            "Recruiting session",
            "#recruiting",
            lambda p: p.hasRecruitingEvent,
            settings.RECRUITING_DATA_DEADLINE,
            lambda s: s.recruitingStatus,
        ),
        (
            "Parcel",
            "#parcel",
            lambda p: p.hasPackets,
            settings.PARCEL_DATA_DEADLINE,
            lambda s: s.packetsStatus,
        ),
        (
            "Advertisement in printed program",
            "#printed-program",
            lambda p: p.hasProgramAd,
            settings.PRINTED_PROGRAM_DATA_DEADLINE,
            lambda s: STATUS_COMPLETE if s.programAd else STATUS_MISSING,
        ),
        (
            "Advertisement text for printed program",
            "#printed-program",
            lambda p: p.hasProgramAdText,
            settings.PRINTED_PROGRAM_DATA_DEADLINE,
            lambda s: STATUS_COMPLETE if s.programAdText != "" else STATUS_MISSING,
        ),
        (
            "Booth personnel",
            "/participants",
            lambda p: p.hasParticipants,
            settings.PARTICIPANTS_DEADLINE,
            lambda s: s.participantsStatus,
        ),
    ]

    def toJSON(self):
        return {
            "name": self.contact.companyName,
            "package": self.package.toJSON(),
            "homepage": self.homepage,
            "logo": self.logo.url if self.logo else "",
            "hpText-en": self.hpTextEN,
            "hpText-de": self.hpTextDE,
            "programAd-text": self.programAdText,
            "programAd-url": self.programAd.url if self.programAd else "",
        }


class SponsoringParticipants(models.Model):
    project = models.ForeignKey(Sponsoring, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isAdmin = models.BooleanField(default=False)
