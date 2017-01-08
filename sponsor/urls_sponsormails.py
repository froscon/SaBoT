from django.conf.urls import include, url

from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from sponsor.models import SponsorMail
from sabot.decorators import user_is_staff

urlpatterns = [
	url(r'^new',
		user_is_staff(CreateView.as_view(
			model = SponsorMail,
			fields = [
				"mailTemplateName",
				"template",
				"mailSubject",
				"attachments",
			],
			template_name = "sponsor/mail/update.html",
			success_url = "list")),
		name = "sponsormail_new"),
	url(r'^(?P<pk>[0-9]+)$',
		user_is_staff(UpdateView.as_view(
			model = SponsorMail,
			fields = [
				"mailTemplateName",
				"template",
				"mailSubject",
				"attachments",
			],
			template_name = "sponsor/mail/update.html",
			success_url = "list")),
		name = "sponsormail_update"),
	url(r'^list/?',
		user_is_staff(ListView.as_view(
			queryset = SponsorMail.objects.all(),
			template_name = "sponsor/mail/list.html")),
			name="sponsormail_list"),
	url(r'^del/(?P<pk>[0-9]+)$',
		user_is_staff(DeleteView.as_view(
			model = SponsorMail,
			template_name= "sponsor/mail/del.html",
			success_url="../list")),
			name="sponsormail_del"),
]
