import datetime
import tempfile
from decimal import Decimal
from datetime import date
import os


from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from invoice import odtemplate
from sabot.utils import random_filename_upload
import sponsor.models

from drafthorse.models.accounting import ApplicableTradeTax
from drafthorse.models.document import Document
from drafthorse.models.note import IncludedNote
from drafthorse.models.party import TaxRegistration
from drafthorse.models.payment import PaymentTerms
from drafthorse.models.tradelines import LineItem
from drafthorse.pdf import attach_xml

class DocumentTemplate(models.Model):
    DOC_CHOICES = (("INVOICE", _("Invoice template")), ("OFFER", _("Offer template")))

    description = models.CharField(
        max_length=128, verbose_name=_("Description for the invoice template")
    )
    template = models.FileField(
        upload_to=random_filename_upload("invoice_templates"),
        verbose_name=_("Invoice template file (odt)"),
    )
    docType = models.CharField(
        max_length=16,
        choices=DOC_CHOICES,
        verbose_name=_("Type of this document template"),
    )

    def __str__(self):
        return self.description


class YearlyInvoiceCounters(models.Model):
    year = models.PositiveIntegerField(
        verbose_name=_("The year this counter belongs to")
    )
    counter = models.PositiveIntegerField(verbose_name=_("The current counter value"))

    @classmethod
    def get_next_counter(cls):
        # check if a counter for this year already exists
        try:
            cntr = cls.objects.get(year=datetime.date.today().year)
        except cls.DoesNotExist:
            cntr = cls(year=datetime.date.today().year, counter=0)
            cntr.save()
        return cntr.counter + 1

    @classmethod
    def update_counter(cls, new_max):
        try:
            cntr = cls.objects.get(year=datetime.date.today().year)
        except cls.DoesNotExist:
            cntr = cls(year=datetime.date.today().year, counter=new_max)
        cntr.counter = new_max
        cntr.save()


class Invoice(models.Model):
    invoiceNumber = models.CharField(
        max_length=64, unique=True, db_index=True, verbose_name=_("Invoice number")
    )
    invoiceAmount = models.DecimalField(
        max_digits=32,
        decimal_places=2,
        editable=False,
        verbose_name=_("Invoice amount"),
    )
    creationDate = models.DateField(
        auto_now_add=True, editable=False, verbose_name=_("Creation date")
    )
    dueDate = models.DateField(verbose_name=_("Due date"))
    payed = models.BooleanField(
        default=False, editable=False, verbose_name=_("This invoice is payed.")
    )
    sponsoring = models.OneToOneField(
        sponsor.models.Sponsoring,
        editable=False,
        null=True,
        related_name="invoice",
        verbose_name=_("Sponsoring package belonging to this invoice"),
        on_delete=models.SET_NULL,
    )
    pdf = models.FileField(
        upload_to="skinvoices",
        blank=True,
        null=True,
        editable=False,
        verbose_name=_("Invoice pdf"),
    )
    template = models.ForeignKey(
        DocumentTemplate,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Template to use for this invoice"),
    )
    rtTicketRef = models.PositiveIntegerField(
        blank=True,
        null=True,
        editable=False,
        verbose_name=_("RT Ticket reference for sending this invoice"),
    )

    class PDFRenderingError(Exception):
        pass

    def getInvoiceFilename(self):
        return "{}.pdf".format(self.invoiceNumber.replace("/", "_"))

    @property
    def billing_reference(self):
        if self.sponsoring.billingReferenceOptOut:
            return str(self.sponsoring.id)
        else:
            return self.sponsoring.billingReference

    def render_pdf(self):
        context = {
            "POSTAL_ADDRESS": self.sponsoring.getBillingAddress(),
            "INVOICE_NUMBER": self.invoiceNumber,
            "INVOICE_REF": self.billing_reference,
            "DUE_DATE": self.dueDate.strftime("%d.%m.%Y"),
            "PACKAGE_NAME": self.sponsoring.package.name,
            "PACKAGE_DESCRIPTION": "\n".join(self.sponsoring.getPacketDescription()),
            "VAT": str(settings.INVOICE_VAT),
            "PRICE_NET": str(self.sponsoring.package.getPriceNet()),
            "PRICE_GROSS": str(self.sponsoring.package.getPriceGross()),
            "VAT_TOTAL": str(self.sponsoring.package.getVATAmount()),
        }
        temp = odtemplate.ODTTemplate(self.template.template.path)
        temp.render(context)
        invoice_pdf_dir = settings.MEDIA_ROOT / "invoice_pdfs"
        if not invoice_pdf_dir.exists():
            invoice_pdf_dir.mkdir()
        pdfpath = invoice_pdf_dir / self.getInvoiceFilename()
        with tempfile.TemporaryDirectory() as d:
            pdfa = os.path.join(d, "tmp.pdf")
            temp.savePDFA(pdfa)
            self._amend_zugferd(pdfa, pdfpath)
        self.pdf.name = "invoice_pdfs/" + self.getInvoiceFilename()
        self.save()

    def _amend_zugferd(self, input_file, output_file):
        total = self.sponsoring.package.getPriceGross()
        tax_total = self.sponsoring.package.getVATAmount()

        doc = Document()
        doc.context.guideline_parameter.id = "urn:cen.eu:en16931:2017#conformant#urn:factur-x.eu:1p0:extended"
        doc.header.id = self.invoiceNumber
        doc.header.type_code = "380"
        doc.header.name = "RECHNUNG"
        doc.header.issue_date_time = date.today()
        doc.header.languages.add("de")

        doc.trade.agreement.seller.name = settings.CONFERENCE_ORGANIZER
        doc.trade.agreement.seller.address.country_id = settings.CONFERENCE_ORGANIZER_COUNTRY_CODE
        doc.trade.agreement.seller.address.country_subdivision = settings.CONFERENCE_ORGANIZER_COUNTRY_SUBDIVISION

        doc.trade.agreement.buyer.name = self.sponsoring.contact.companyName
        doc.trade.agreement.buyer.address.country_id = "DE"
        doc.trade.settlement.invoicee.name = self.sponsoring.contact.companyName
        doc.trade.settlement.payee.name = self.sponsoring.contact.companyName

        doc.trade.settlement.currency_code = "EUR"
        doc.trade.settlement.payment_means.type_code = "ZZZ"


        doc.trade.agreement.seller_order.issue_date_time = datetime.datetime.now(datetime.timezone.utc)
        doc.trade.agreement.seller_order.issuer_assigned_id = self.invoiceNumber
        doc.trade.agreement.buyer_order.issue_date_time = datetime.datetime.now(datetime.timezone.utc)
        doc.trade.agreement.buyer_order.issuer_assigned_id = self.billing_reference
        doc.trade.settlement.advance_payment.received_date = datetime.datetime.now(datetime.timezone.utc)
        doc.trade.agreement.customer_order.issue_date_time = datetime.datetime.now(datetime.timezone.utc)

        li = LineItem()
        li.document.line_id = "1"
        li.product.name = self.sponsoring.package.name
        li.product.description = "\n".join(self.sponsoring.getPacketDescription())
        li.agreement.gross.amount = total
        li.agreement.gross.basis_quantity = (Decimal("1.0000"), "C62")  # C62 == pieces
        li.agreement.net.amount = total - tax_total
        li.agreement.net.basis_quantity = (Decimal("1.0000"), "C62") # C62 == pieces
        li.delivery.billed_quantity = (Decimal("1.0000"), "C62")  # C62 == pieces
        li.settlement.trade_tax.type_code = "VAT"
        li.settlement.trade_tax.category_code = "S"
        li.settlement.trade_tax.rate_applicable_percent = Decimal(settings.INVOICE_VAT)
        li.settlement.monetary_summation.total_amount = total - tax_total
        doc.trade.items.add(li)

        trade_tax = ApplicableTradeTax()
        trade_tax.calculated_amount = tax_total
        trade_tax.basis_amount = total - tax_total
        trade_tax.type_code = "VAT"
        trade_tax.category_code = "S"
        trade_tax.rate_applicable_percent = Decimal(settings.INVOICE_VAT)
        doc.trade.settlement.trade_tax.add(trade_tax)

        pt = PaymentTerms()
        pt.description = "Just send your money."
        pt.due = self.dueDate
        doc.trade.settlement.terms.add(pt)

        doc.trade.agreement.seller.tax_registrations.add(
            TaxRegistration(
                id=("VA", settings.CONFERENCE_ORGANIZER_VAT_ID)
            )
        )

        doc.trade.settlement.monetary_summation.line_total = total - tax_total
        doc.trade.settlement.monetary_summation.charge_total = Decimal("0.00")
        doc.trade.settlement.monetary_summation.allowance_total = Decimal("0.00")
        doc.trade.settlement.monetary_summation.tax_basis_total = total - tax_total
        doc.trade.settlement.monetary_summation.tax_total = (tax_total, "EUR")
        doc.trade.settlement.monetary_summation.grand_total = total
        doc.trade.settlement.monetary_summation.due_amount = total

        # Generate XML file
        xml = doc.serialize(schema="FACTUR-X_EXTENDED")

        # Attach XML to an existing PDF.
        # Note that the existing PDF should be compliant to PDF/A-3!
        # You can validate this here: https://www.pdf-online.com/osa/validate.aspx
        with open(input_file, "rb") as original_file:
            new_pdf_bytes = attach_xml(original_file.read(), xml)

        with open(output_file, "wb") as f:
            f.write(new_pdf_bytes)


class SMSKaufenSnailMailJob(models.Model):
    sponsoring = models.OneToOneField(
        sponsor.models.Sponsoring,
        related_name="snailmailinvoice",
        verbose_name=_("Sponsoring package belonging to this snail mailing job"),
        on_delete=models.CASCADE,
    )
    jobid = models.PositiveIntegerField(verbose_name=_("SMSKaufen job identifier"))
    joberror = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=_("Error description of a potential processing error"),
    )
    success = models.BooleanField(
        default=False, verbose_name=_("The mail was successfully sent.")
    )
