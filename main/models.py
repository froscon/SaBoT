from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _



# Create your models here.
class ConferenceYear(models.Model):
	@staticmethod
	def ensureExists(current):
		try:
			current = ConferenceYear.objects.get(year=current)
		except ConferenceYear.DoesNotExist:
			cy = ConferenceYear(year=current)
			cy.save()

	def __str__(self):
		return str(self.year)

	def __unicode__(self):
		return unicode(self.year)

	year = models.PositiveIntegerField(editable=False, unique=True, verbose_name=_("Conference year that exists in our database"))
