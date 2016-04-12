import json

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from sponsor.models import Sponsoring
from exhibitor.models import Exhibitor
from devroom.models import Devroom

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
