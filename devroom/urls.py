from django.urls import path, reverse
from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Sum

from devroom.forms import DevroomGeneralForm, DevroomDescriptionForm, DevroomProgramForm
from devroom.models import Devroom, DevroomParticipants
from devroom.views import SetRoomView
from sabot.decorators import user_is_staff
from sabot.multiYear import (
    YSListView,
    YSXMLListView,
    YSOwnerSettingCreateView,
    getActiveYear,
)
from sabot.views import (
    ParticipantsView,
    OwnerSettingCreateView,
    PermCheckUpdateView,
    EmailOutputView,
    XMLListView,
    MultipleListView,
    PropertySetterView,
    PermCheckPropertySetterView,
    PermCheckSimpleDeleteView,
    ArchiveCreatorView,
)


urlpatterns = [
    path(
        "new",
        login_required(
            YSOwnerSettingCreateView.as_view(
                model=Devroom,
                form_class=DevroomGeneralForm,
                template_name="devroom/create.html",
                success_url="/devrooms/{id}",
            )
        ),
        name="devroom_new",
    ),
    path(
        "<int:pk>",
        login_required(
            PermCheckUpdateView.as_view(
                model=Devroom,
                form_class=DevroomGeneralForm,
                template_name="devroom/general.html",
                success_url="/devrooms/{id}",
            )
        ),
        name="devroom_update_general",
    ),
    path(
        "<int:pk>/description",
        login_required(
            PermCheckUpdateView.as_view(
                model=Devroom,
                form_class=DevroomDescriptionForm,
                template_name="devroom/description.html",
                success_url="/devrooms/{id}/description",
            )
        ),
        name="devroom_update_texts",
    ),
    path(
        "<int:pk>/program",
        login_required(
            PermCheckUpdateView.as_view(
                model=Devroom,
                form_class=DevroomProgramForm,
                template_name="devroom/program.html",
                success_url="/devrooms/{id}/program",
            )
        ),
        name="devroom_update_program",
    ),
    path(
        "<int:pk>/participants",
        login_required(
            ParticipantsView.as_view(
                object_class=Devroom,
                connection_table_class=DevroomParticipants,
                template_name="devroom/participants.html",
            )
        ),
        name="devroom_participants",
    ),
    path(
        "<int:pk>/accept",
        user_is_staff(
            PropertySetterView.as_view(
                model=Devroom,
                property_name="accepted",
                property_value=True,
                next_view="devroom_list",
            )
        ),
        name="devroom_accept",
    ),
    path(
        "<int:pk/unaccept",
        user_is_staff(
            PropertySetterView.as_view(
                model=Devroom,
                property_name="accepted",
                property_value=False,
                next_view="devroom_list",
            )
        ),
        name="devroom_unaccept",
    ),
    path(
        "<int:pk>/setroom",
        user_is_staff(SetRoomView.as_view(success_url="/devrooms/list")),
        name="devroom_setroom",
    ),
    path(
        "participants/remove/<int:pk>",
        login_required(
            PermCheckSimpleDeleteView.as_view(
                model=DevroomParticipants,
                permission_checker=lambda obj, user: obj.project.has_write_permission(
                    user
                ),
                redirect=lambda obj, kwargs: reverse(
                    "devroom_participants", kwargs={"pk": obj.project_id}
                ),
            )
        ),
        name="devroom_participants_delete",
    ),
    path(
        "participants/makeadmin/<int:pk>",
        login_required(
            PermCheckPropertySetterView.as_view(
                model=DevroomParticipants,
                permission_checker=lambda obj, user: obj.project.has_write_permission(
                    user
                ),
                property_name="isAdmin",
                property_value=True,
                redirect=lambda obj, kwargs: reverse(
                    "devroom_participants", kwargs={"pk": obj.project_id}
                ),
            )
        ),
        name="devroom_participants_make_admin",
    ),
    path(
        "participants/revokeadmin/<int:pk>",
        login_required(
            PermCheckPropertySetterView.as_view(
                model=DevroomParticipants,
                permission_checker=lambda obj, user: obj.project.has_write_permission(
                    user
                ),
                property_name="isAdmin",
                property_value=False,
                redirect=lambda obj, kwargs: reverse(
                    "devroom_participants", kwargs={"pk": obj.project_id}
                ),
            )
        ),
        name="devroom_participants_revoke_admin",
    ),
    path(
        "list",
        user_is_staff(
            YSListView.as_view(
                queryset=Devroom.objects.select_related(),
                template_name="devroom/list.html",
            )
        ),
        name="devroom_list",
    ),
    path(
        "del/<int:pk>",
        user_is_staff(
            DeleteView.as_view(
                model=Devroom,
                template_name="devroom/del.html",
                success_url="/devrooms/list",
            )
        ),
        name="devroom_del",
    ),
    path(
        "export/adminmail",
        user_is_staff(
            EmailOutputView.as_view(
                queryset=lambda req, kwargs: User.objects.filter(
                    Q(
                        devroomparticipants__isAdmin=True,
                        devroomparticipants__project__accepted=True,
                        devroomparticipants__project__year=getActiveYear(req),
                    )
                    | Q(devrooms__accepted=True, devrooms__year=getActiveYear(req))
                ).distinct(),
                template_name="mail.html",
            )
        ),
        name="devroom_export_adminmail",
    ),
    path(
        "export/allmail",
        user_is_staff(
            EmailOutputView.as_view(
                queryset=lambda req, kwargs: User.objects.filter(
                    Q(
                        devroomparticipants__project__accepted=True,
                        devroomparticipants__project__year=getActiveYear(req),
                    )
                    | Q(devrooms__accepted=True, devrooms__year=getActiveYear(req))
                ).distinct(),
                template_name="mail.html",
            )
        ),
        name="devroom_export_allmail",
    ),
    path(
        "export/xml",
        user_is_staff(
            YSXMLListView.as_view(
                queryset=Devroom.objects.select_related().filter(accepted=True),
                template_name="devroom/xmlexport.html",
            )
        ),
        name="devroom_export_xml",
    ),
]
