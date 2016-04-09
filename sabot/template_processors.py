import datetime
from django.conf import settings

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
		'SPONSOR_MAIL' : settings.SPONSOR_MAIL
	}
