from functools import partial

from django.contrib.auth.decorators import login_required
from django.urls import reverse, path

from parcel.forms import UserParcelForm
from parcel.models import Parcel
from parcel.views import LinkedParcelListView, LinkedParcelCreateView
from sponsor.models import Sponsoring

from sabot.views import PermCheckDeleteView, PermCheckUpdateView, MultipleListView

def parcel_delete_next(obj, kwargs):
	if obj.sponsoring is not None:
		return reverse("sponsor_update", kwargs = { "pk" : obj.sponsoring_id }) + "#parcel"
	else:
		return reverse("parcel_list")


urlpatterns = [
	path('<int:lpk>/list',
		login_required(LinkedParcelListView.as_view(
			linked_model = Sponsoring,
			template_name = "sponsor/tracking.html")),
		name="sponsor_parcel_tracking"),
	path('<int:lpk>/new',
		login_required(LinkedParcelCreateView.as_view(
			linked_model = Sponsoring,
			model = Parcel,
			form_class = UserParcelForm,
			template_name = "parcel/user/update.html",
			success_url = lambda obj, kwargs : reverse("sponsor_parcel_tracking", kwargs = { "lpk" : obj.ownerId }))),
		name="sponsor_parcel_new"),
	path('<int:pk>/remove',
		login_required(PermCheckDeleteView.as_view(
			model = Parcel,
			template_name= "parcel/admin/del.html",
			redirect = lambda obj, kwargs: reverse("sponsor_parcel_tracking", kwargs = { "lpk" : obj.ownerId }) )),
		name="sponsor_parcel_del"),
	path('<int:pk>',
		login_required(PermCheckUpdateView.as_view(
			model = Parcel,
			form_class = UserParcelForm,
			template_name = "parcel/user/update.html",
			success_url = lambda obj, kwargs : reverse("sponsor_parcel_tracking", kwargs = { "lpk" : obj.ownerId }))),
		name="sponsor_parcel_update"),
]
