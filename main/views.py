from django.views.generic import TemplateView, RedirectView
from sponsor.models import Sponsoring
from exhibitor.models import Exhibitor, ExhibitorParticipants
from devroom.models import Devroom, DevroomParticipants
from django.db.models import Q
from django.core.urlresolvers import reverse

class OverviewView(TemplateView):
	def get_context_data(self, **kwargs):
		context = super(OverviewView, self).get_context_data(**kwargs)
		context["user"] = self.request.user
		context["user_sponsorings"] = Sponsoring.objects.filter(participants=self.request.user)
		context["user_exhibitors"] = Exhibitor.objects.filter(Q(owner=self.request.user) | Q(participants=self.request.user)).distinct()
		context["user_devrooms"] = Devroom.objects.filter(Q(owner=self.request.user) | Q(participants=self.request.user)).distinct()

		return context

class WayfinderView(RedirectView):
	permanent = False

	def get_redirect_url(self, **kwargs):
		# check if this is a sponsor account:
		try:
			sponsor = Sponsoring.objects.get(owner=self.request.user)
			return reverse("sponsor_overview", kwargs = { "pk" : sponsor.id })
		except:
			return reverse("overview")

