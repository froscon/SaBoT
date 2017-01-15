import datetime
from django.conf import settings

from sabot.multiYear import getActiveYear
from main.models import ConferenceYear


allYears = None

def getAllYears():
	# Cache this value. If this changes it is ok for me to restart the
	# django app.
	global allYears
	if allYears is None:
		ConferenceYear.ensureExists(settings.CURRENT_CONFERENCE_YEAR)
		allYears = [cy.year for cy in ConferenceYear.objects.all()]

	return allYears

def dates_processor(request):
    return {
		'reg_deadline_booth' : settings.REGISTRATION_DEADLINE,
		'reg_deadline_room' : settings.REGISTRATION_DEADLINE,
		'change_deadline' : settings.CHANGES_DEADLINE,
		'date_today' : datetime.date.today(),
	}

def settings_processor(request):
	return {
		'RT_TICKET_URL' : settings.RT_TICKET_URL,
		'SPONSOR_MAIL' : settings.SPONSOR_MAIL,
		'INSTALL_MAIN_URL' : settings.INSTALL_MAIN_URL,
		'CONFERENCE_NAME' : settings.CONFERENCE_NAME
	}

def active_year_processor(request):
	return {
		'active_year' : getActiveYear(request),
		'all_years' : getAllYears(),
	}
