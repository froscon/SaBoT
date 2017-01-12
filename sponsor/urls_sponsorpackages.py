from django.conf.urls import include, url
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Sum
from django.views.generic import ListView, DeleteView, CreateView, UpdateView

from sabot.decorators import user_is_staff
from sabot.multiYear import YSListView, YSXMLListView, YSCreateView
from sabot.views import ParticipantsView, OwnerSettingCreateView, PermCheckUpdateView, EmailOutputView, XMLListView, MultipleListView, PropertySetterView, PermCheckPropertySetterView, PermCheckSimpleDeleteView, ArchiveCreatorView
from sponsor.forms import SponsorContactForm, SponsorPackageForm
from sponsor.models import Sponsoring, SponsoringParticipants, SponsorContact, SponsorPackage
from sponsor.views import SponsorCreateView, SponsorUpdateView, SponsorEmailingView, sponsorMailPreview, SponsorContactResetEmailView, loadResponseInfoFromRT

urlpatterns = [
	url(r'^new',
		user_is_staff(YSCreateView.as_view(
			model = SponsorPackage,
			form_class = SponsorPackageForm,
			template_name = "sponsor/package/update.html",
			success_url = "{id}")),
		name = "sponsorpackage_new"),
	url(r'^(?P<pk>[0-9]+)$',
		user_is_staff(UpdateView.as_view(
			model = SponsorPackage,
			form_class = SponsorPackageForm,
			template_name = "sponsor/package/update.html",
			success_url = "list")),
		name = "sponsorpackage_update"),
	url(r'^list/?',
		user_is_staff(YSListView.as_view(
			queryset = SponsorPackage.objects.all(),
			template_name = "sponsor/package/list.html")),
			name="sponsorpackage_list"),
	url(r'^del/(?P<pk>[0-9]+)$',
		user_is_staff(DeleteView.as_view(
			model = SponsorPackage,
			template_name= "sponsor/package/del.html",
			success_url="../list")),
			name="sponsorpackage_del"),
	url(r'^export/xml',
		user_is_staff(YSXMLListView.as_view(
			queryset = SponsorPackage.objects.all(),
			template_name = "sponsor/package/xmlexport.html")),
			name="sponsorpackage_export_xml"),
]
