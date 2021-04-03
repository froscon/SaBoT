from django.urls import reverse
from django.db.models import Q
from django.views.generic import TemplateView, RedirectView

from devroom.models import Devroom, DevroomParticipants
from exhibitor.models import Exhibitor, ExhibitorParticipants
from sabot.multiYear import getActiveYear
from sponsor.models import Sponsoring

class OverviewView(TemplateView):
	def get_context_data(self, **kwargs):
		context = super(OverviewView, self).get_context_data(**kwargs)
		context["user"] = self.request.user
		context["user_sponsorings"] = Sponsoring.objects.filter(
			owner=self.request.user,
			commitment=True,
			year=getActiveYear(self.request),
		)
		context["user_sponsoring_member"] = Sponsoring.objects.filter(participants=self.request.user,year=getActiveYear(self.request))
		context["user_exhibitors"] = Exhibitor.objects.filter(year=getActiveYear(self.request)).filter(Q(owner=self.request.user) | Q(participants=self.request.user)).distinct()
		context["user_devrooms"] = Devroom.objects.filter(year=getActiveYear(self.request)).filter(Q(owner=self.request.user) | Q(participants=self.request.user)).distinct()

		return context

class WayfinderView(RedirectView):
	permanent = False

	def get_redirect_url(self, **kwargs):
		# check if this is a sponsor account:
		try:
			sponsor = Sponsoring.objects.get(
				owner=self.request.user,
				commitment=True,
				year=getActiveYear(self.request),
			)
			return reverse("sponsor_overview", kwargs = { "pk" : sponsor.id })
		except: # if there is none or multiple sponsorships
			return reverse("overview")

