from functools import partial

from django.conf.urls import include, url

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Sum
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, TemplateView

from invoice.forms import OfferForm
from sponsor.forms import SponsorContactForm, SponsorPackageForm
from sponsor.helpers import sponsor_filesanitize
from sponsor.models import Sponsoring, SponsoringParticipants, SponsorContact, SponsorPackage
from sponsor.views import SponsorCreateView, SponsorUpdateView, SponsorEmailingView, sponsorMailPreview, SponsorContactResetEmailView, loadResponseInfoFromRT

from sabot.views import ParticipantsView, OwnerSettingCreateView, PermCheckUpdateView, EmailOutputView, XMLListView, MultipleListView, PropertySetterView, PermCheckPropertySetterView, PermCheckSimpleDeleteView, ArchiveCreatorView, PermCheckDeleteView, PermCheckDetailView
from sabot.decorators import user_is_staff

urlpatterns = [
	url(r'^new/(?P<pk>[0-9]+)$',
		user_is_staff(SponsorCreateView.as_view()), name="sponsor_new"),
	url(r'^(?P<pk>[0-9]+)/?$',
		login_required(SponsorUpdateView.as_view()), name="sponsor_update"),
	url(r'^(?P<pk>[0-9]+)/participants$',
		login_required(ParticipantsView.as_view(
			object_class = Sponsoring,
			connection_table_class = SponsoringParticipants,
			template_name = "sponsor/participants.html")),
		name="sponsor_participants"),
	url(r'^(?P<pk>[0-9]+)/overview$',
		login_required(PermCheckDetailView.as_view(
			model = Sponsoring,
			template_name = "sponsor/overview.html")),
		name="sponsor_overview"),
	url(r'^(?P<pk>[0-9]+)/faq$',
		login_required(TemplateView.as_view(
			template_name = "sponsor/internalFaqPage.html")),
		name="sponsor_faq"),
	url(r'^participants/remove/(?P<pk>[0-9]+)$',
		login_required(PermCheckSimpleDeleteView.as_view(
			model = SponsoringParticipants,
			permission_checker = lambda obj, user: obj.project.has_write_permission(user),
			redirect = lambda obj, kwargs: reverse("sponsor_participants", kwargs = { "pk" : obj.project_id }) )),
		name="sponsor_participants_delete"),
	url(r'^list/?',
		user_is_staff(MultipleListView.as_view(
			template_name = "sponsor/sponsoring/list.html",
			template_params = {
				"object_list" : Sponsoring.objects.select_related(),
				"moneyRaised" : lambda req, kwargs : Sponsoring.objects.filter(commitment=True).aggregate(total_sum=Sum("package__price"))["total_sum"],
				"wantRecruiting" : lambda req, kwargs : Sponsoring.objects.filter(wantRecruting=True,commitment=True).count(),
				"noRecruiting" : lambda req, kwargs : Sponsoring.objects.filter(wantRecruting=False,commitment=True).count(),
				"canRecruiting" : lambda req, kwargs : Sponsoring.objects.filter(package__hasRecruitingEvent=True,commitment=True).count(),
				"wantBooth" : lambda req, kwargs : Sponsoring.objects.filter(wantBooth=True,commitment=True).count(),
				"noBooth" : lambda req, kwargs : Sponsoring.objects.filter(wantBooth=False,commitment=True).count(),
				"canBooth" : lambda req, kwargs : Sponsoring.objects.filter(package__hasBooth=True,commitment=True).count(),
				"offerForm" : lambda req, kwargs : OfferForm(),
			})),
			name="sponsor_list"),
	url(r'^del/(?P<pk>[0-9]+)$',
		user_is_staff(DeleteView.as_view(model = Sponsoring, template_name= "sponsor/sponsoring/del.html", success_url="/sponsors/list") ),name="sponsor_del"),
	url(r'^export/adminmail',
		user_is_staff(EmailOutputView.as_view(
			queryset = User.objects.annotate(num_spon=Count("sponsorings")).filter(num_spon__gt=0).distinct(),
			template_name = "mail.html")),
			name="sponsor_export_adminmail"),
	url(r'^export/allmail',
		user_is_staff(EmailOutputView.as_view(
			queryset = User.objects.annotate(num_spon=Count("sponsorings"), num_part=Count("sponsorparticipation")).filter( Q(num_part__gt=0)).distinct(),
			template_name = "mail.html")),
			name="sponsor_export_allmail"),
	url(r'^export/boothmail',
		user_is_staff(EmailOutputView.as_view(
			queryset = User.objects.filter(sponsorparticipation__package__hasBooth=True).distinct(),
			template_name = "mail.html")),
			name="sponsor_export_boothmail"),
	url(r'^export/recruitingmail',
		user_is_staff(EmailOutputView.as_view(
			queryset = User.objects.filter(sponsorparticipation__package__hasRecruitingEvent=True).distinct(),
			template_name = "mail.html")),
			name="sponsor_export_recruitingmail"),
	url(r'^export/xml',
		user_is_staff(XMLListView.as_view(
			queryset = Sponsoring.objects.select_related(),
			template_name = "sponsor/sponsoring/xmlexport.html")),
			name="sponsor_export_xml"),
	url(r'^export/logos',
		user_is_staff(ArchiveCreatorView.as_view(
			filename = "sponsorlogos.tar.bz2",
			filelist = lambda : filter(lambda x : x is not None, map(partial(sponsor_filesanitize,"logo"), Sponsoring.objects.select_related())) )),
			name="sponsor_export_logos"),
	url(r'^export/programad',
		user_is_staff(ArchiveCreatorView.as_view(
			filename = "sponsorads.tar.bz2",
			filelist = lambda : filter(lambda x : x is not None, map(partial(sponsor_filesanitize,"programAd"), Sponsoring.objects.select_related())) )),
			name="sponsor_export_programad"),
	url(r'^parcel/', include('sponsor.urls_parcel')),
]
