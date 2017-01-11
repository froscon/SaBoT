from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class ConferenceYear(models.Model):
	year = models.PositiveIntegerField(editable=False, verbose_name=_("Conference year that exists in our database"))
