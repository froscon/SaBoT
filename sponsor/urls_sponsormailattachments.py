from django.conf.urls import include, url

from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from sponsor.models import SponsorMailAttachment
from sabot.decorators import user_is_staff

urlpatterns = [
	url(r'^new',
		user_is_staff(CreateView.as_view(
			model = SponsorMailAttachment,
			template_name = "sponsor/mailattachment/update.html",
			success_url = "list")),
		name = "sponsormailattachment_new"),
	url(r'^(?P<pk>[0-9]+)$',
		user_is_staff(UpdateView.as_view(
			model = SponsorMailAttachment,
			template_name = "sponsor/mailattachment/update.html",
			success_url = "list")),
		name = "sponsormailattachment_update"),
	url(r'^list/?',
		user_is_staff(ListView.as_view(
			queryset = SponsorMailAttachment.objects.all(),
			template_name = "sponsor/mailattachment/list.html")),
			name="sponsormailattachment_list"),
	url(r'^del/(?P<pk>[0-9]+)$',
		user_is_staff(DeleteView.as_view(
			model = SponsorMailAttachment,
			template_name= "sponsor/mailattachment/del.html",
			success_url="../list")),
			name="sponsormailattachment_del"),
]
