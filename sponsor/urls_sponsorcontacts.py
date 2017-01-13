import datetime

from django.conf.urls import include, url
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Sum

from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from sponsor.views import SponsorCreateView, SponsorUpdateView, SponsorEmailingView, sponsorMailPreview, SponsorContactResetEmailView, loadResponseInfoFromRT
from sponsor.forms import SponsorContactForm, SponsorPackageForm
from sponsor.models import Sponsoring, SponsoringParticipants, SponsorContact, SponsorPackage
from sabot.views import ParticipantsView, OwnerSettingCreateView, PermCheckUpdateView, EmailOutputView, XMLListView, MultipleListView, PropertySetterView, PermCheckPropertySetterView, PermCheckSimpleDeleteView, ArchiveCreatorView
from sabot.decorators import user_is_staff

urlpatterns = [
	url(r'^new',
		user_is_staff(CreateView.as_view(
			model = SponsorContact,
			form_class = SponsorContactForm,
			template_name = "sponsor/contact/update.html",
			success_url = "./{id}")),
		name = "sponsorcontact_new"),
	url(r'^(?P<pk>[0-9]+)$',
		user_is_staff(UpdateView.as_view(
			model = SponsorContact,
			form_class = SponsorContactForm,
			template_name = "sponsor/contact/update.html",
			success_url = "list#contact-{id}")),
		name = "sponsorcontact_update"),
	url(r'^list/?',
		user_is_staff(ListView.as_view(
			queryset = SponsorContact.objects.select_related(),
			template_name = "sponsor/contact/list.html")),
			name="sponsorcontact_list"),
	url(r'^(?P<pk>[0-9]+)/mailed$',
		user_is_staff(PropertySetterView.as_view(
			model = SponsorContact,
			property_name = "lastMailed",
			property_value = lambda req, **kwargs : datetime.date.today(),
			redirect = "/sponsorcontacts/list#contact-{id}")),
		name="sponsorcontact_set_mailed"),
	url(r'^del/(?P<pk>[0-9]+)$',
		user_is_staff(DeleteView.as_view(
			model = SponsorContact,
			template_name = "sponsor/contact/del.html",
			success_url="../list")),
			name="sponsorcontact_del"),
	url(r'^mailpreview/(?P<pk>[0-9]+)$',
		user_is_staff(sponsorMailPreview),
		name="sponsorcontact_mail_preview"),
	url(r'^mail/?',
		user_is_staff(SponsorEmailingView.as_view()),
		name="sponsorcontact_mail"),
	url(r'^export/xml',
		user_is_staff(XMLListView.as_view(
			queryset = SponsorContact.objects.select_related(),
			template_name = "sponsor/contact/xmlexport.html")),
			name="sponsorcontact_export_xml"),
	url(r'^reset/?',
		user_is_staff(SponsorContactResetEmailView.as_view(
			template_name = "sponsor/contactMailer/confirmEmailReset.html",
			next_view = "sponsorcontact_list")),
			name="sponsorcontact_email_reset"),
	url(r'^rt-update/?',
		user_is_staff(loadResponseInfoFromRT),
			name="sponsorcontact_response_update"),
]
