from django.conf.urls import url
from django.urls import path
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from parcel.forms import ParcelAdminForm
from parcel.models import Parcel
from parcel.views import queryParcelOwners, packageQuickStore
from sabot.decorators import user_is_finance, user_is_staff
from sabot.multiYear import getActiveYear, YSCreateView
from sabot.views import MultipleListView
from sponsor.models import Sponsoring

urlpatterns = [
    path(
        "list",
        user_is_staff(
            MultipleListView.as_view(
                template_params={
                    "object_list": lambda req, kwargs: Sponsoring.objects.filter(
                        year=getActiveYear(req)
                    ).select_related(),
                    "parcel_list": lambda req, kwargs: Parcel.objects.filter(
                        year=getActiveYear(req)
                    ).select_related(),
                },
                template_name="parcel/admin/list.html",
            )
        ),
        name="parcel_list",
    ),
    path(
        "new",
        user_is_staff(
            YSCreateView.as_view(
                model=Parcel,
                form_class=ParcelAdminForm,
                template_name="parcel/admin/update.html",
                success_url="parcel_list",
            )
        ),
        name="parcel_new",
    ),
    path(
        "<int:pk>",
        user_is_staff(
            UpdateView.as_view(
                model=Parcel,
                form_class=ParcelAdminForm,
                template_name="parcel/admin/update.html",
                success_url="list",
            )
        ),
        name="parcel_update",
    ),
    path(
        "del/<int:pk>",
        user_is_staff(
            DeleteView.as_view(
                model=Parcel,
                template_name="parcel/admin/del.html",
                success_url="../list",
            )
        ),
        name="parcel_del",
    ),
    path("query_owners", user_is_staff(queryParcelOwners), name="parcel_query_owners"),
    path("quick_store", user_is_staff(packageQuickStore), name="parcel_quick_store"),
]
