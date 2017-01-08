from functools import partial

from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Count, Q, Sum
from django.views.generic import ListView, DeleteView, CreateView, UpdateView

from parcel.forms import UserParcelForm
from parcel.models import Parcel
from parcel.views import LinkedParcelListView, LinkedParcelCreateView
from sponsor.models import Sponsoring

from sabot.decorators import user_is_staff
from sabot.views import PermCheckDeleteView, PermCheckUpdateView, MultipleListView

def parcel_delete_next(obj, kwargs):
	if obj.sponsoring is not None:
		return reverse("sponsor_update", kwargs = { "pk" : obj.sponsoring_id }) + "#parcel"
	else:
		return reverse("parcel_list")


urlpatterns = [
	url(r'^(?P<lpk>[0-9]+)/list$',
		login_required(LinkedParcelListView.as_view(
			linked_model = Sponsoring,
			template_name = "sponsor/tracking.html")),
		name="sponsor_parcel_tracking"),
	url(r'^(?P<lpk>[0-9]+)/new$',
		login_required(LinkedParcelCreateView.as_view(
			linked_model = Sponsoring,
			model = Parcel,
			form_class = UserParcelForm,
			template_name = "parcel/user/update.html",
			success_url = lambda obj, kwargs : reverse("sponsor_parcel_tracking", kwargs = { "lpk" : obj.ownerId }))),
		name="sponsor_parcel_new"),
	url(r'^(?P<pk>[0-9]+)/remove$',
		login_required(PermCheckDeleteView.as_view(
			model = Parcel,
			template_name= "parcel/admin/del.html",
			redirect = lambda obj, kwargs: reverse("sponsor_parcel_tracking", kwargs = { "lpk" : obj.ownerId }) )),
		name="sponsor_parcel_del"),
	url(r'^(?P<pk>[0-9]+)$',
		login_required(PermCheckUpdateView.as_view(
			model = Parcel,
			form_class = UserParcelForm,
			template_name = "parcel/user/update.html",
			success_url = lambda obj, kwargs : reverse("sponsor_parcel_tracking", kwargs = { "lpk" : obj.ownerId }))),
		name="sponsor_parcel_update"),
]
