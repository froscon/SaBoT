from django.conf import settings
from django.views.generic import ListView, CreateView

from sabot.views import EmailOutputView, XMLListView

def getActiveYear(request):
	return request.session.get("currentYear", settings.CURRENT_CONFERENCE_YEAR)


class RestrictToSelectedYearMixin(object):
	def get_queryset(self):
		queryset = super(RestrictToSelectedYearMixin, self).get_queryset()
		selectedYear = getActiveYear(self.request)
		return queryset.filter(year=selectedYear)

def makeYearSelected(cls):
	class YS(RestrictToSelectedYearMixin, cls):
		pass
	return YS

YSEmailOutputView = makeYearSelected(EmailOutputView)
YSXMLListView = makeYearSelected(XMLListView)
YSListView = makeYearSelected(ListView)


class YSOwnerSettingCreateView(CreateView):
	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.owner = self.request.user
		self.object.year = getActiveYear(self.requst)
		self.object.save()
		return redirect(self.get_success_url())

class YSCreateView(CreateView):
	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.year = getActiveYear(self.requst)
		self.object.save()
		return redirect(self.get_success_url())
