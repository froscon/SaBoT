from functools import partial

from django.conf.urls import patterns, include, url

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Sum

from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from sponsor.views import ParcelCreateView, ParcelUpdateView
from sponsor.forms import SponsorParcelAdminForm
from sponsor.models import SponsorParcel, Sponsoring

from sabot.views import PermCheckDeleteView, MultipleListView
from sabot.decorators import user_is_staff

def parcel_delete_next(obj, kwargs):
	if obj.sponsoring is not None:
		return reverse("sponsor_update", kwargs = { "pk" : obj.sponsoring_id }) + "#parcel"
	else:
		return reverse("parcel_list")


urlpatterns = patterns('',
	url(r'^S-(?P<spk>[0-9]+)/newpacket$',
		login_required(ParcelCreateView.as_view()),
		name="parcel_add"),
	url(r'^newpacket$',
		user_is_staff(CreateView.as_view(
			model = SponsorParcel,
			form_class = SponsorParcelAdminForm,
			template_name = "sponsor/parcel/update.html",
			success_url="list")),
		name="parcel_add_admin"),
	url(r'^(?P<pk>[0-9]+)/view$',
		login_required(ParcelUpdateView.as_view()),
		name="parcel_update"),
	url(r'^(?P<pk>[0-9]+)/delete$',
		login_required(PermCheckDeleteView.as_view(
			model = SponsorParcel,
			redirect = lambda obj, kwargs: reverse("sponsor_update", kwargs = { "pk" : obj.sponsoring_id }) + "#parcel",
			template_name = "sponsor/parcel/del.html"
		)),
		name="parcel_del"),
	url(r'^list',
		user_is_staff(MultipleListView.as_view(
			template_params = {
				"object_list" : Sponsoring.objects.select_related(),
				"parcel_list" : SponsorParcel.objects.select_related(),
			},
			template_name = "sponsor/parcel/list.html")),
		name="parcel_list"),
)
