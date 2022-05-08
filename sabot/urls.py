from django.conf.urls import include
from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from main.views import OverviewView, WayfinderView
from sabot.multiYear import setActiveYearView

urlpatterns = [
    ############# PORTAL PAGE #################
    path("", login_required(WayfinderView.as_view()), name="homepage"),
    path(
        "overview",
        login_required(OverviewView.as_view(template_name="main/homepage.html")),
        name="overview",
    ),
    path("faq", TemplateView.as_view(template_name="sponsor/publicFaqPage.html")),
    ########## MULTIYEAR SUPPORT #############
    re_path("^setYear/(?P<year>\\d{4})$", login_required(setActiveYearView)),
    ############ INCLUDE APPS ################
    path(r"accounts/", include("account.urls")),
    path("accounts/", include("django_registration.backends.activation.urls")),
    path(r"sponsors/", include("sponsor.urls_sponsors")),
    path(r"parcel/", include("parcel.urls")),
    path(r"sponsorcontacts/", include("sponsor.urls_sponsorcontacts")),
    path(r"sponsorpackages/", include("sponsor.urls_sponsorpackages")),
    path(r"sponsordjangotemplates/", include("sponsor.urls_sponsordjangotemplates")),
    path(r"sponsormails/", include("sponsor.urls_sponsormails")),
    path(r"sponsormailattachments/", include("sponsor.urls_sponsormailattachments")),
    path(r"exhibitors/", include("exhibitor.urls")),
    path(r"devrooms/", include("devroom.urls")),
    path(r"documenttemplate/", include("invoice.urls_documenttemplate")),
    path(r"invoice/", include("invoice.urls_invoice")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
