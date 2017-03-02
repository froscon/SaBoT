import datetime

from django.conf.urls import url
from django.views.generic import ListView

from invoice import views
from invoice.models import Invoice
from sabot.decorators import user_is_finance, user_is_staff
from sabot.multiYear import getActiveYear
from sabot.views import PropertySetterView, MultipleListView, ObjectFileDownloader
from sponsor.models import Sponsoring

urlpatterns = [
	url(r"^invoices$",
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
	url(r"^create/(?P<spk>\d+)$",
		user_is_finance(views.InvoiceCreateUpdateView.as_view(
			next_view="invoice_overview")),
		name = "invoice_create"),
	url(r"^downloadinvoice/(?P<pk>\d+)$",
		user_is_staff(ObjectFileDownloader.as_view(
			model = Invoice,
			upload_field = "pdf",
			content_type = "application/pdf")),
		name = "invoice_download"),
	url(r"^sendinvoice/(?P<spk>\d+)$",
		user_is_finance(views.RTinvoiceView.as_view()),
		name = "invoice_sendinvoice"),
	url(r"^snailmailinvoice/(?P<spk>\d+)$",
		user_is_finance(views.InvoiceSnailMailView.as_view()),
		name = "invoice_snailmailinvoice"),
	url(r"^snailmailstatussink/(?P<invId>[0-9a-zA-Z-]+_?)$",
		views.SMSKaufenStatusUpdate,
		name = "invoice_snailmailstatus"),
	url(r"^getinvoicemailtemplate/(?P<spk>\d+)$",
		user_is_finance(views.InvoiceEmailTemplate),
		name = "invoice_invoicemailtemplate"),
	url(r"^genoffer-odt/(?P<spk>\d+)-(?P<template>\d+)$",
		user_is_staff(views.generateSponsoringOffer),
		name = "invoice_generate_offer_odt"),
	url(r"^genoffer-pdf/(?P<spk>\d+)-(?P<template>\d+)$",
		user_is_staff(views.generateSponsoringOfferPDF),
		name = "invoice_generate_offer_pdf"),
	url(r'^(?P<pk>[0-9]+)/pay$',
		user_is_finance(PropertySetterView.as_view(
			model = Invoice,
			property_name = "payed",
			property_value = True,
			next_view = "invoice_overview")),
		name="invoice_markpayed"),
	url(r'^(?P<pk>[0-9]+)/unpay$',
		user_is_finance(PropertySetterView.as_view(
			model = Invoice,
			property_name = "payed",
			property_value = False,
			next_view = "invoice_overview")),
		name="invoice_marknotpayed"),
]
