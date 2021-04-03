import datetime

from django.urls import path

from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from sponsor.views import SponsorCreateView, SponsorUpdateView, SponsorEmailingView, sponsorMailPreview, SponsorContactResetEmailView, loadResponseInfoFromRT
from sponsor.forms import SponsorContactForm, SponsorPackageForm
from sponsor.models import Sponsoring, SponsoringParticipants, SponsorContact, SponsorPackage
from sabot.views import ParticipantsView, OwnerSettingCreateView, PermCheckUpdateView, EmailOutputView, XMLListView, MultipleListView, PropertySetterView, PermCheckPropertySetterView, PermCheckSimpleDeleteView, ArchiveCreatorView
from sabot.decorators import user_is_staff

urlpatterns = [
	path('new',
		user_is_staff(CreateView.as_view(
			model = SponsorContact,
			form_class = SponsorContactForm,
			template_name = "sponsor/contact/update.html",
			success_url = "./{id}")),
		name = "sponsorcontact_new"),
	path('<int:pk>',
		user_is_staff(UpdateView.as_view(
			model = SponsorContact,
			form_class = SponsorContactForm,
			template_name = "sponsor/contact/update.html",
			success_url = "list#contact-{id}")),
		name = "sponsorcontact_update"),
	path('list',
		user_is_staff(ListView.as_view(
			queryset = SponsorContact.objects.select_related(),
			template_name = "sponsor/contact/list.html")),
			name="sponsorcontact_list"),
	path('<int:pk>/mailed',
		user_is_staff(PropertySetterView.as_view(
			model = SponsorContact,
			property_name = "lastMailed",
			property_value = lambda req, **kwargs : datetime.date.today(),
			redirect = "/sponsorcontacts/list#contact-{id}")),
		name="sponsorcontact_set_mailed"),
	path('del/<int:pk>',
		user_is_staff(DeleteView.as_view(
			model = SponsorContact,
			template_name = "sponsor/contact/del.html",
			success_url="../list")),
			name="sponsorcontact_del"),
	path('mailpreview/<int:pk>',
		user_is_staff(sponsorMailPreview),
		name="sponsorcontact_mail_preview"),
	path('mail',
		user_is_staff(SponsorEmailingView.as_view()),
		name="sponsorcontact_mail"),
	path('export/xml',
		user_is_staff(XMLListView.as_view(
			queryset = SponsorContact.objects.select_related(),
			template_name = "sponsor/contact/xmlexport.html")),
			name="sponsorcontact_export_xml"),
	path('reset',
		user_is_staff(SponsorContactResetEmailView.as_view(
			template_name = "sponsor/contactMailer/confirmEmailReset.html",
			next_view = "sponsorcontact_list")),
			name="sponsorcontact_email_reset"),
	path('rt-update',
		user_is_staff(loadResponseInfoFromRT),
			name="sponsorcontact_response_update"),
]
