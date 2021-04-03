from django.urls import path, reverse
from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Sum

from exhibitor.forms import ExhibitorGeneralForm, ExhibitorDescriptionForm, ExhibitorBoothForm
from exhibitor.models import Exhibitor, ExhibitorParticipants
from sabot.decorators import user_is_staff
from sabot.multiYear import YSListView, YSXMLListView, YSOwnerSettingCreateView, getActiveYear
from sabot.views import ParticipantsView, OwnerSettingCreateView, PermCheckUpdateView, EmailOutputView, XMLListView, MultipleListView, PropertySetterView, PermCheckPropertySetterView, PermCheckSimpleDeleteView, ArchiveCreatorView


urlpatterns = [
	path('new',
		login_required(YSOwnerSettingCreateView.as_view(
			model = Exhibitor,
			form_class = ExhibitorGeneralForm,
			template_name = "exhibitor/create.html",
			success_url = "/exhibitors/{id}")),
		name="exhibitor_new"),
	path('<int:pk>',
		login_required(PermCheckUpdateView.as_view(
			model = Exhibitor,
			form_class = ExhibitorGeneralForm,
			template_name = "exhibitor/general.html",
			success_url = "/exhibitors/{id}")),
		name = "exhibitor_update_general"),
	path('<int:pk>/description',
		login_required(PermCheckUpdateView.as_view(
			model = Exhibitor,
			form_class = ExhibitorDescriptionForm,
			template_name = "exhibitor/description.html",
			success_url = "/exhibitors/{id}/description")),
		name = "exhibitor_update_texts"),
	path('<int:pk>/booth',
		login_required(PermCheckUpdateView.as_view(
			model = Exhibitor,
			form_class = ExhibitorBoothForm,
			template_name = "exhibitor/booth.html",
			success_url = "/exhibitors/{id}/booth")),
		name = "exhibitor_update_booth"),
	path('<int:pk>/participants',
		login_required(ParticipantsView.as_view(
			object_class = Exhibitor,
			connection_table_class = ExhibitorParticipants,
			template_name = "exhibitor/participants.html")),
		name="exhibitor_participants"),
	path('<int:pk>/accept',
		user_is_staff(PropertySetterView.as_view(
			model = Exhibitor,
			property_name = "accepted",
			property_value = True,
			next_view = "exhibitor_list")),
		name="exhibitor_accept"),
	path('<int:pk>/unaccept',
		user_is_staff(PropertySetterView.as_view(
			model = Exhibitor,
			property_name = "accepted",
			property_value = False,
			next_view = "exhibitor_list")),
		name="exhibitor_unaccept"),
	path('participants/remove/<int:pk>',
		login_required(PermCheckSimpleDeleteView.as_view(
			model = ExhibitorParticipants,
			permission_checker = lambda obj, user: obj.project.has_write_permission(user),
			redirect = lambda obj, kwargs: reverse("exhibitor_participants", kwargs = { "pk" : obj.project_id }) )),
		name="exhibitor_participants_delete"),
	path('participants/makeadmin/<int:pk>',
		login_required(PermCheckPropertySetterView.as_view(
			model = ExhibitorParticipants,
			permission_checker = lambda obj, user: obj.project.has_write_permission(user),
			property_name = "isAdmin",
			property_value = True,
			redirect = lambda obj, kwargs: reverse("exhibitor_participants", kwargs = { "pk" : obj.project_id }) )),
		name="exhibitor_participants_make_admin"),
	path('participants/revokeadmin/<int:pk>',
		login_required(PermCheckPropertySetterView.as_view(
			model = ExhibitorParticipants,
			permission_checker = lambda obj, user: obj.project.has_write_permission(user),
			property_name = "isAdmin",
			property_value = False,
			redirect = lambda obj, kwargs: reverse("exhibitor_participants", kwargs = { "pk" : obj.project_id }) )),
		name="exhibitor_participants_revoke_admin"),
	path('list+planning',
		user_is_staff(YSListView.as_view(
			queryset = Exhibitor.objects.select_related(),
			template_name = "exhibitor/list+planning.html")),
			name="exhibitor_list_planning"),
	path('list',
		user_is_staff(YSListView.as_view(
			queryset = Exhibitor.objects.select_related(),
			template_name = "exhibitor/list.html")),
			name="exhibitor_list"),
	path('del/<int:pk>',
		user_is_staff(DeleteView.as_view(
			model = Exhibitor,
			template_name= "exhibitor/del.html",
			success_url="/exhibitors/list")),
			name="exhibitor_del"),
	path('export/adminmail',
		user_is_staff(EmailOutputView.as_view(
			queryset = lambda req, kwargs : User.objects.filter(
				Q(exhibitorparticipants__isAdmin=True,
				  exhibitorparticipants__project__accepted=True,
				  exhibitorparticipants__project__year=getActiveYear(req)) |
				Q(exhibitors__accepted=True,exhibitors__year=getActiveYear(req))
				).distinct(),
			template_name = "mail.html")),
			name="exhibitor_export_adminmail"),
	path('export/allmail',
		user_is_staff(EmailOutputView.as_view(
			queryset = lambda req, kwargs : User.objects.filter(
				Q(exhibitorparticipants__project__accepted=True,
				  exhibitorparticipants__project__year=getActiveYear(req)) |
				Q(exhibitors__accepted=True,exhibitors__year=getActiveYear(req))
				).distinct(),
			template_name = "mail.html")),
			name="exhibitor_export_allmail"),
	path('export/xml',
		user_is_staff(YSXMLListView.as_view(
			queryset = Exhibitor.objects.select_related().filter(accepted=True),
			template_name = "exhibitor/xmlexport.html")),
			name="exhibitor_export_xml"),
]
