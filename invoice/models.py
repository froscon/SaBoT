import datetime
from decimal import Decimal
import os


from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

import sponsor.models
from invoice import odtemplate

class DocumentTemplate(models.Model):
	DOC_CHOICES = (
		('INVOICE', _("Invoice template")),
		('OFFER', _("Offer template"))
	)

	description = models.CharField(max_length=128, verbose_name=_("Description for the invoice template"))
	template = models.FileField(upload_to="invoice_templates", verbose_name=_("Invoice template file (odt)"))
	docType = models.CharField(max_length=16, choices=DOC_CHOICES, verbose_name=_("Type of this document template"))



	def __unicode__(self):
		return self.description

class YearlyInvoiceCounters(models.Model):
	year = models.PositiveIntegerField(verbose_name=_("The year this counter belongs to"))
	counter = models.PositiveIntegerField(verbose_name=_("The current counter value"))

	@classmethod
	def get_next_counter(cls):
		# check if a counter for this year already exists
		try:
			cntr = cls.objects.get(year=datetime.date.today().year)
		except cls.DoesNotExist:
			cntr = cls(year=datetime.date.today().year,counter=0)
			cntr.save()
		return cntr.counter+1

	@classmethod
	def update_counter(cls,new_max):
		try:
			cntr = cls.objects.get(year=datetime.date.today().year)
		except cls.DoesNotExist:
			cntr = cls(year=datetime.date.today().year,counter=new_max)
		cntr.counter=new_max
		cntr.save()

class Invoice(models.Model):
	invoiceNumber = models.CharField(max_length=64, unique=True, db_index=True, verbose_name=_("Invoice number"))
	invoiceAmount = models.DecimalField(max_digits=32, decimal_places=2, editable=False, verbose_name=_("Invoice amount"))
	creationDate = models.DateField(auto_now_add=True, editable=False, verbose_name=_("Creation date"))
	dueDate = models.DateField(verbose_name=_("Due date"))
	payed = models.BooleanField(default=False, editable=False, verbose_name=_("This invoice is payed."))
	sponsoring = models.OneToOneField(sponsor.models.Sponsoring, editable=False, related_name="invoice", verbose_name=_("Sponsoring package belonging to this invoice"))
	pdf = models.FileField(upload_to="skinvoices", blank=True, null=True, editable=False, verbose_name=_("Invoice pdf"))
	template = models.ForeignKey(DocumentTemplate,null=True, on_delete=models.SET_NULL, verbose_name=_("Template to use for this invoice"))
	rtTicketRef = models.PositiveIntegerField(blank=True, null=True, editable=False, verbose_name=_("RT Ticket reference for sending this invoice"))

	class PDFRenderingError(Exception):
		pass

	def getInvoiceFilename(self):
		return "{}.pdf".format(self.invoiceNumber.replace("/","_"))

	def render_pdf(self):
		if self.sponsoring.billingReferenceOptOut:
			billRef = str(self.sponsoring.id)
		else:
			billRef = self.sponsoring.billingReference
		context = {
			"POSTAL_ADDRESS" : self.sponsoring.getBillingAddress(),
			"INVOICE_NUMBER" : self.invoiceNumber,
			"INVOICE_REF" : billRef,
			"DUE_DATE" : self.dueDate.strftime("%d.%m.%Y"),
			"PACKAGE_NAME" : self.sponsoring.package.name,
			"PACKAGE_DESCRIPTION" : "\n".join(self.sponsoring.getPacketDescription()),
			"VAT" : str(settings.INVOICE_VAT),
			"PRICE_NET" : str(self.sponsoring.package.price.quantize(Decimal("0.01"))),
			"PRICE_GROSS" : str(self.sponsoring.package.getPriceGross()),
			"VAT_TOTAL" : str(self.sponsoring.package.getVATAmount()),
		}
		temp = odtemplate.ODTTemplate(self.template.template.path)
		temp.render(context)
		if not os.path.exists(settings.MEDIA_ROOT + "invoice_pdfs"):
			os.mkdir(settings.MEDIA_ROOT + "invoice_pdfs")
		pdfpath = settings.MEDIA_ROOT + "invoice_pdfs/" + self.getInvoiceFilename()
		temp.savePDF(pdfpath)
		self.pdf.name = "invoice_pdfs/" + self.getInvoiceFilename()
		self.save()

class SMSKaufenSnailMailJob(models.Model):
	sponsoring = models.OneToOneField(sponsor.models.Sponsoring, related_name="snailmailinvoice", verbose_name=_("Sponsoring package belonging to this snail mailing job"))
	jobid = models.PositiveIntegerField(verbose_name=_("SMSKaufen job identifier"))
	joberror = models.CharField(max_length=256, blank=True, verbose_name=_("Error description of a potential processing error"))
	success = models.BooleanField(default=False, verbose_name=_("The mail was successfully sent."))


