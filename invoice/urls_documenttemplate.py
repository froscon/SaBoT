from django.conf.urls import include, url
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Sum
from django.views.generic import ListView, DeleteView, CreateView, UpdateView

from sabot.decorators import user_is_staff
from invoice.models import DocumentTemplate

urlpatterns = [
	url(r'^new',
		user_is_staff(CreateView.as_view(
			model = DocumentTemplate,
			fields = [
				"description",
				"template",
				"docType",
			],
			template_name = "invoice/documenttemplate/update.html",
			success_url = "{id}")),
		name = "documenttemplate_new"),
	url(r'^(?P<pk>[0-9]+)$',
		user_is_staff(UpdateView.as_view(
			model = DocumentTemplate,
			fields = [
				"description",
				"template",
				"docType",
			],
			template_name = "invoice/documenttemplate/update.html",
			success_url = "{id}")),
		name = "documenttemplate_update"),
	url(r'^list/?',
		user_is_staff(ListView.as_view(
			queryset = DocumentTemplate.objects.all(),
			template_name = "invoice/documenttemplate/list.html")),
			name="documenttemplate_list"),
	url(r'^del/(?P<pk>[0-9]+)$',
		user_is_staff(DeleteView.as_view(
			model = DocumentTemplate,
			template_name= "invoice/documenttemplate/del.html",
			success_url="../list")),
			name="documenttemplate_del"),
]
