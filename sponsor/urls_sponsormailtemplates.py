from django.conf.urls import patterns, include, url

from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from sponsor.models import SponsorMailTemplate
from sabot.decorators import user_is_staff

urlpatterns = patterns('',
	url(r'^new',
		user_is_staff(CreateView.as_view(
			model = SponsorMailTemplate,
			template_name = "sponsor/mailtemplate/update.html",
			success_url = "list")),
		name = "sponsormailtemplate_new"),
	url(r'^(?P<pk>[0-9]+)$',
		user_is_staff(UpdateView.as_view(
			model = SponsorMailTemplate,
			template_name = "sponsor/mailtemplate/update.html",
			success_url = "list")),
		name = "sponsormailtemplate_update"),
	url(r'^list/?',
		user_is_staff(ListView.as_view(
			queryset = SponsorMailTemplate.objects.all(),
			template_name = "sponsor/mailtemplate/list.html")),
			name="sponsormailtemplate_list"),
	url(r'^del/(?P<pk>[0-9]+)$',
		user_is_staff(DeleteView.as_view(
			model = SponsorMailTemplate,
			template_name= "sponsor/mailtemplate/del.html",
			success_url="../list")),
			name="sponsormailtemplate_del"),
)
