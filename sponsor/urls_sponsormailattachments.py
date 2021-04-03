from django.urls import path

from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from sponsor.models import SponsorMailAttachment
from sabot.decorators import user_is_staff

urlpatterns = [
	path('new',
		user_is_staff(CreateView.as_view(
			model = SponsorMailAttachment,
			fields = [
				"name",
				"attachment",
			],
			template_name = "sponsor/mailattachment/update.html",
			success_url = "list")),
		name = "sponsormailattachment_new"),
	path('<int:pk>',
		user_is_staff(UpdateView.as_view(
			model = SponsorMailAttachment,
			fields = [
				"name",
				"attachment",
			],
			template_name = "sponsor/mailattachment/update.html",
			success_url = "list")),
		name = "sponsormailattachment_update"),
	path('list',
		user_is_staff(ListView.as_view(
			queryset = SponsorMailAttachment.objects.all(),
			template_name = "sponsor/mailattachment/list.html")),
			name="sponsormailattachment_list"),
	path('del/<int:pk>',
		user_is_staff(DeleteView.as_view(
			model = SponsorMailAttachment,
			template_name= "sponsor/mailattachment/del.html",
			success_url="../list")),
			name="sponsormailattachment_del"),
]
