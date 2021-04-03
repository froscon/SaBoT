import datetime

from django.urls import path, re_path

from invoice import views
from invoice.models import Invoice
from sabot.decorators import user_is_finance, user_is_staff
from sabot.multiYear import getActiveYear
from sabot.views import PropertySetterView, MultipleListView, ObjectFileDownloader
from sponsor.models import Sponsoring

urlpatterns = [
	path("invoices",
		user_is_staff(MultipleListView.as_view(
			template_params = {
				"object_list" : lambda req, kwargs : Sponsoring.objects.select_related().filter(
					year=getActiveYear(req),
					commitment=True,
					clearedForBilling=True
				),
				"today" : lambda req, kwargs : datetime.date.today(),
			},
			template_name = "invoice/invoices.html")),
		name = "invoice_overview"),
	path("create/<int:spk>",
		user_is_finance(views.InvoiceCreateUpdateView.as_view(
			next_view="invoice_overview")),
		name = "invoice_create"),
	path("downloadinvoice/<int:pk>",
		user_is_staff(ObjectFileDownloader.as_view(
			model = Invoice,
			upload_field = "pdf",
			content_type = "application/pdf")),
		name = "invoice_download"),
	path("sendinvoice/<int:spk>",
		user_is_finance(views.RTinvoiceView.as_view()),
		name = "invoice_sendinvoice"),
	path("snailmailinvoice/<int:spk>",
		user_is_finance(views.InvoiceSnailMailView.as_view()),
		name = "invoice_snailmailinvoice"),
	re_path("^snailmailstatussink/(?P<invId>[0-9a-zA-Z-]+_?)$",
		views.SMSKaufenStatusUpdate,
		name = "invoice_snailmailstatus"),
	path("getinvoicemailtemplate/<int:spk>",
		user_is_finance(views.InvoiceEmailTemplate),
		name = "invoice_invoicemailtemplate"),
	path("genoffer-odt/<int:spk>-<int:template>",
		user_is_staff(views.generateSponsoringOffer),
		name = "invoice_generate_offer_odt"),
	path("genoffer-pdf/<int:spk>-<int:template>",
		user_is_staff(views.generateSponsoringOfferPDF),
		name = "invoice_generate_offer_pdf"),
	path('<int:pk>/pay',
		user_is_finance(PropertySetterView.as_view(
			model = Invoice,
			property_name = "payed",
			property_value = True,
			next_view = "invoice_overview")),
		name="invoice_markpayed"),
	path('<int:pk>/unpay',
		user_is_finance(PropertySetterView.as_view(
			model = Invoice,
			property_name = "payed",
			property_value = False,
			next_view = "invoice_overview")),
		name="invoice_marknotpayed"),
]
