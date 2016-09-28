from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from main.views import OverviewView, WayfinderView

urlpatterns = patterns('',
############# PORTAL PAGE #################

	url(r"^$", 	login_required(WayfinderView.as_view()), name = "homepage"),
	url(r"^overview$",
		login_required(OverviewView.as_view(
			template_name = "main/homepage.html")),
		name = "overview"),
	url(r"^faq$", TemplateView.as_view(template_name="sponsor/publicFaqPage.html")),

############ INCLUDE APPS ################
	url(r'^accounts/', include('account.urls')),
	url(r'^accounts/', include('registration.backends.default.urls')),

	url(r'^sponsors/', include('sponsor.urls_sponsors')),
	url(r'^parcel/', include('parcel.urls')),
	url(r'^sponsorcontacts/', include('sponsor.urls_sponsorcontacts')),
	url(r'^sponsorpackages/', include('sponsor.urls_sponsorpackages')),
	url(r'^sponsordjangotemplates/', include('sponsor.urls_sponsordjangotemplates')),
	url(r'^sponsormails/', include('sponsor.urls_sponsormails')),
	url(r'^sponsormailattachments/', include('sponsor.urls_sponsormailattachments')),
	url(r'^exhibitors/', include('exhibitor.urls')),
	url(r'^devrooms/', include('devroom.urls')),
	#url(r'^ticket/', include('ticket.urls')),
	url(r'^documenttemplate/', include('invoice.urls_documenttemplate')),
	url(r'^invoice/', include('invoice.urls_invoice')),
)

if settings.LOCAL:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	from django.contrib.staticfiles.urls import staticfiles_urlpatterns
	urlpatterns += staticfiles_urlpatterns()
