from django.urls import path

from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from sponsor.models import SponsorMailTemplate
from sabot.decorators import user_is_staff

urlpatterns = [
	path('new',
		user_is_staff(CreateView.as_view(
			model = SponsorMailTemplate,
			fields = [
				"templateName",
				"template",
			],
			template_name = "sponsor/dbtemplate/update.html",
			success_url = "list")),
		name = "sponsordbtemplate_new"),
	path('<int:pk>',
		user_is_staff(UpdateView.as_view(
			model = SponsorMailTemplate,
			fields = [
				"templateName",
				"template",
			],
			template_name = "sponsor/dbtemplate/update.html",
			success_url = "list")),
		name = "sponsordbtemplate_update"),
	path('list',
		user_is_staff(ListView.as_view(
			queryset = SponsorMailTemplate.objects.all(),
			template_name = "sponsor/dbtemplate/list.html")),
			name="sponsordbtemplate_list"),
	path('del/<int:pk>',
		user_is_staff(DeleteView.as_view(
			model = SponsorMailTemplate,
			template_name= "sponsor/dbtemplate/del.html",
			success_url="../list")),
			name="sponsordbtemplate_del"),
]
