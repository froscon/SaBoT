from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView

from main.models import ConferenceYear
from sabot.views import EmailOutputView, XMLListView, JSONListView


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


YSJSONListView = makeYearSelected(JSONListView)
YSXMLListView = makeYearSelected(XMLListView)
YSListView = makeYearSelected(ListView)


class YSOwnerSettingCreateView(CreateView):
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.year = getActiveYear(self.request)
        self.object.save()
        return redirect(self.get_success_url())


class YSCreateView(CreateView):
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.year = getActiveYear(self.request)
        self.object.save()
        return redirect(self.get_success_url())


def setActiveYearView(request, year):
    if request.method != "POST":
        raise Http404
    try:
        cy = ConferenceYear.objects.get(year=year)
    except ConferenceYear.DoesNotExist:
        raise Http404
    request.session["currentYear"] = cy.year
    return HttpResponse("")
