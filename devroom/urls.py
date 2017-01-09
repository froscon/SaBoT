from django.conf.urls import include, url
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Sum

from sabot.views import ParticipantsView, OwnerSettingCreateView, PermCheckUpdateView, EmailOutputView, XMLListView, MultipleListView, PropertySetterView, PermCheckPropertySetterView, PermCheckSimpleDeleteView, ArchiveCreatorView
from sabot.decorators import user_is_staff
from devroom.models import Devroom, DevroomParticipants
from devroom.forms import DevroomGeneralForm, DevroomDescriptionForm, DevroomProgramForm
from devroom.views import SetRoomView


urlpatterns = [
	url(r'^new$',
		login_required(OwnerSettingCreateView.as_view(
			model = Devroom,
			form_class = DevroomGeneralForm,
			template_name = "devroom/create.html",
			success_url = "/devrooms/{id}")),
		name="devroom_new"),
	url(r'^(?P<pk>[0-9]+)$',
		login_required(PermCheckUpdateView.as_view(
			model = Devroom,
			form_class = DevroomGeneralForm,
			template_name = "devroom/general.html",
			success_url = "/devrooms/{id}")),
		name = "devroom_update_general"),
	url(r'^(?P<pk>[0-9]+)/description$',
		login_required(PermCheckUpdateView.as_view(
			model = Devroom,
			form_class = DevroomDescriptionForm,
			template_name = "devroom/description.html",
			success_url = "/devrooms/{id}/description")),
		name = "devroom_update_texts"),
	url(r'^(?P<pk>[0-9]+)/program$',
		login_required(PermCheckUpdateView.as_view(
			model = Devroom,
			form_class = DevroomProgramForm,
			template_name = "devroom/program.html",
			success_url = "/devrooms/{id}/program")),
		name = "devroom_update_program"),
	url(r'^(?P<pk>[0-9]+)/participants$',
		login_required(ParticipantsView.as_view(
			object_class = Devroom,
			connection_table_class = DevroomParticipants,
			template_name = "devroom/participants.html")),
		name="devroom_participants"),
	url(r'^(?P<pk>[0-9]+)/accept$',
		user_is_staff(PropertySetterView.as_view(
			model = Devroom,
			property_name = "accepted",
			property_value = True,
			next_view = "devroom_list")),
		name="devroom_accept"),
	url(r'^(?P<pk>[0-9]+)/unaccept$',
		user_is_staff(PropertySetterView.as_view(
			model = Devroom,
			property_name = "accepted",
			property_value = False,
			next_view = "devroom_list")),
		name="devroom_unaccept"),
	url(r'^(?P<pk>[0-9]+)/setroom$',
		user_is_staff(SetRoomView.as_view(
			success_url = "/devrooms/list")),
		name="devroom_setroom"),
	url(r'^participants/remove/(?P<pk>[0-9]+)$',
		login_required(PermCheckSimpleDeleteView.as_view(
			model = DevroomParticipants,
			permission_checker = lambda obj, user: obj.project.has_write_permission(user),
			redirect = lambda obj, kwargs: reverse("devroom_participants", kwargs = { "pk" : obj.project_id }) )),
		name="devroom_participants_delete"),
	url(r'^participants/makeadmin/(?P<pk>[0-9]+)$',
		login_required(PermCheckPropertySetterView.as_view(
			model = DevroomParticipants,
			permission_checker = lambda obj, user: obj.project.has_write_permission(user),
			property_name = "isAdmin",
			property_value = True,
			redirect = lambda obj, kwargs: reverse("devroom_participants", kwargs = { "pk" : obj.project_id }) )),
		name="devroom_participants_make_admin"),
	url(r'^participants/revokeadmin/(?P<pk>[0-9]+)$',
		login_required(PermCheckPropertySetterView.as_view(
			model = DevroomParticipants,
			permission_checker = lambda obj, user: obj.project.has_write_permission(user),
			property_name = "isAdmin",
			property_value = False,
			redirect = lambda obj, kwargs: reverse("devroom_participants", kwargs = { "pk" : obj.project_id }) )),
		name="devroom_participants_revoke_admin"),
	url(r'^list/?',
		user_is_staff(ListView.as_view(
			queryset = Devroom.objects.select_related(),
			template_name = "devroom/list.html")),
			name="devroom_list"),
	url(r'^del/(?P<pk>[0-9]+)$',
		user_is_staff(DeleteView.as_view(
			model = Devroom,
			template_name= "devroom/del.html",
			success_url="/devrooms/list")),
			name="devroom_del"),
	url(r'^export/adminmail',
		user_is_staff(EmailOutputView.as_view(
			queryset = User.objects.filter(Q(devroomparticipants__isAdmin=True,devroomparticipants__project__accepted=True) | Q(devrooms__accepted=True)).distinct(),
			template_name = "mail.html")),
			name="devroom_export_adminmail"),
	url(r'^export/allmail',
		user_is_staff(EmailOutputView.as_view(
			queryset = User.objects.filter(Q(devroomparticipants__project__accepted=True) | Q(devrooms__accepted=True)).distinct(),
			template_name = "mail.html")),
			name="devroom_export_allmail"),
	url(r'^export/xml',
		user_is_staff(XMLListView.as_view(
			queryset = Devroom.objects.select_related().filter(accepted=True),
			template_name = "devroom/xmlexport.html")),
			name="devroom_export_xml"),
]
