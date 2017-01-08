from django.conf.urls import include, url

from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from sponsor.models import SponsorMailTemplate
from sabot.decorators import user_is_staff

urlpatterns = [
	url(r'^new',
		user_is_staff(CreateView.as_view(
			model = SponsorMailTemplate,
			template_name = "sponsor/dbtemplate/update.html",
			success_url = "list")),
		name = "sponsordbtemplate_new"),
	url(r'^(?P<pk>[0-9]+)$',
		user_is_staff(UpdateView.as_view(
			model = SponsorMailTemplate,
			template_name = "sponsor/dbtemplate/update.html",
			success_url = "list")),
		name = "sponsordbtemplate_update"),
	url(r'^list/?',
		user_is_staff(ListView.as_view(
			queryset = SponsorMailTemplate.objects.all(),
			template_name = "sponsor/dbtemplate/list.html")),
			name="sponsordbtemplate_list"),
	url(r'^del/(?P<pk>[0-9]+)$',
		user_is_staff(DeleteView.as_view(
			model = SponsorMailTemplate,
			template_name= "sponsor/dbtemplate/del.html",
			success_url="../list")),
			name="sponsordbtemplate_del"),
]
