from django.conf.urls import url
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from parcel.forms import ParcelAdminForm
from parcel.models import Parcel
from parcel.views import queryParcelOwners
from sabot.decorators import user_is_finance, user_is_staff
from sponsor.models import Sponsoring
from sabot.views import MultipleListView

urlpatterns = [
	url(r'^list/?',
		user_is_staff(MultipleListView.as_view(
			template_params = {
				"object_list" : Sponsoring.objects.select_related(),
				"parcel_list" : Parcel.objects.select_related(),
			},
			template_name = "parcel/admin/list.html")),
		name = "parcel_list"),
	url(r'^new',
		user_is_staff(CreateView.as_view(
			model = Parcel,
			form_class = ParcelAdminForm,
			template_name = "parcel/admin/update.html",
			success_url = "list")),
		name = "parcel_new"),
	url(r'^(?P<pk>[0-9]+)$',
		user_is_staff(UpdateView.as_view(
			model = Parcel,
			form_class = ParcelAdminForm,
			template_name = "parcel/admin/update.html",
			success_url = "list")),
		name = "parcel_update"),
	url(r'^del/(?P<pk>[0-9]+)$',
		user_is_staff(DeleteView.as_view(
			model = Parcel,
			template_name= "parcel/admin/del.html",
			success_url="../list")),
		name = "parcel_del"),
	url(r'query_owners',
		user_is_staff(queryParcelOwners),
		name = "parcel_query_owners"),
]
