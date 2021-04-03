from django.urls import path
from django.views.generic import ListView, DeleteView, CreateView, UpdateView

from sabot.decorators import user_is_staff
from sabot.multiYear import YSXMLListView, YSCreateView, getActiveYear
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
from sponsor.forms import SponsorContactForm, SponsorPackageForm, PackagesImporterForm
from sponsor.models import (
    Sponsoring,
    SponsoringParticipants,
    SponsorContact,
    SponsorPackage,
)
from sponsor.views import PackagesImporterView

urlpatterns = [
    path(
        "new",
        user_is_staff(
            YSCreateView.as_view(
                model=SponsorPackage,
                form_class=SponsorPackageForm,
                template_name="sponsor/package/update.html",
                success_url="./{id}",
            )
        ),
        name="sponsorpackage_new",
    ),
    path(
        "<int:pk>",
        user_is_staff(
            UpdateView.as_view(
                model=SponsorPackage,
                form_class=SponsorPackageForm,
                template_name="sponsor/package/update.html",
                success_url="list",
            )
        ),
        name="sponsorpackage_update",
    ),
    path(
        "list",
        user_is_staff(
            MultipleListView.as_view(
                template_name="sponsor/package/list.html",
                template_params={
                    "object_list": lambda req, kwargs: SponsorPackage.objects.filter(
                        year=getActiveYear(req)
                    ),
                    "importerForm": lambda req, kwargs: PackagesImporterForm(),
                },
            )
        ),
        name="sponsorpackage_list",
    ),
    path(
        "del/<int:pk>",
        user_is_staff(
            DeleteView.as_view(
                model=SponsorPackage,
                template_name="sponsor/package/del.html",
                success_url="../list",
            )
        ),
        name="sponsorpackage_del",
    ),
    path(
        "export/xml",
        user_is_staff(
            YSXMLListView.as_view(
                queryset=SponsorPackage.objects.all(),
                template_name="sponsor/package/xmlexport.html",
            )
        ),
        name="sponsorpackage_export_xml",
    ),
    path(
        "import",
        user_is_staff(PackagesImporterView.as_view()),
        name="sponsorpackage_import",
    ),
]
