import json

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, ListView

from devroom.models import Devroom
from exhibitor.models import Exhibitor
from parcel.models import Parcel
from sabot.views import CallableSuccessUrlMixin
from sponsor.models import Sponsoring

def queryParcelOwners(request):
	response = []
	if request.GET.has_key("q"):
		query = request.GET["q"]

		# find companies with matching name
		res = Sponsoring.objects.filter(contact__companyName__icontains=query)
		response = response + [ {
			"identifier" : s.contact.companyName,
			"type" : unicode(_("Sponsor")),
			"contentType_id" : ContentType.objects.get_for_model(Sponsoring).id,
			"obj_id" : s.pk,
			}
			for s in res ]
		res = Exhibitor.objects.filter(projectName__icontains=query)
		response = response + [ {
			"identifier" : p.projectName,
			"type" : unicode(_("Exhibitor")),
			"contentType_id" : ContentType.objects.get_for_model(Exhibitor).id,
			"obj_id" : p.pk,
			}
			for p in res ]
		res = Devroom.objects.filter(projectName__icontains=query)
		response = response + [ {
			"identifier" : p.projectName,
			"type" : unicode(_("Devroom")),
			"contentType_id" : ContentType.objects.get_for_model(Devroom).id,
			"obj_id" : p.pk,
			}
			for p in res ]


	return HttpResponse(json.dumps(response), content_type="application/json")



class LinkedParcelCreateView(CallableSuccessUrlMixin,CreateView):
	linked_model = None

	def form_valid(self, form):
		try:
			linked = self.linked_model.objects.get(pk=self.kwargs["lpk"])
		except self.linked_model.DoesNotExist:
			raise Http404

		if not linked.has_write_permission(self.request.user) and not self.request.user.is_staff:
			raise PermissionDenied

		self.object = form.save(commit=False)
		self.object.owner = linked
		self.object.save()
		return redirect(self.get_success_url())

class LinkedParcelListView(ListView):
	linked_model = None

	@cached_property
	def linked_object(self):
		try:
			linked = self.linked_model.objects.get(pk=self.kwargs["lpk"])
		except self.linked_model.DoesNotExist:
			raise Http404

		if not linked.has_read_permission(self.request.user) and not self.request.user.is_staff:
			raise PermissionDenied
		return linked

	def get_queryset(self):
		linked = self.linked_object

		content_type = ContentType.objects.get_for_model(self.linked_model)
		return Parcel.objects.filter(ownerType=content_type, ownerId=linked.pk)

	def get_context_data(self, **kwargs):
		kwargs = super(LinkedParcelListView, self).get_context_data(**kwargs)
		kwargs["linked_object"] = self.linked_object
		return kwargs
