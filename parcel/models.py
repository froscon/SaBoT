from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from devroom.models import Devroom
from exhibitor.models import Exhibitor
from sponsor.models import Sponsoring

class Parcel(models.Model):
	ownerType = models.ForeignKey(ContentType, null=True, blank=True, verbose_name=_("Type of the owner object"), on_delete=models.SET_NULL)
	ownerId = models.PositiveIntegerField(blank=True, null=True, verbose_name=_("Key of the owner object"))
	owner = GenericForeignKey("ownerType", "ownerId")
	originText = models.CharField(max_length=256, blank=True, verbose_name=_("Name or description of the sender if it is no registered owner"))
	createDate = models.DateField(auto_now_add=True,editable=False, verbose_name=_("Creation date"))
	parcelService = models.CharField(max_length=128, verbose_name=_("Delivery service company"))
	trackingNumber = models.CharField(max_length=128, verbose_name=_("Tracking number"))
	trackingUrl = models.URLField(blank=True, verbose_name=_("Tracking URL (if available)"))
	contentAndUsage = models.TextField(blank=True, verbose_name=_("What is the content of this package? What should we use it for?"))
	received = models.BooleanField(default=False, verbose_name=_("We received this package (tick this and enter storage location once handled)"))
	storageLocation = models.TextField(blank=True, verbose_name=_("Storage location"))

	year = models.PositiveIntegerField(editable=False, verbose_name=_("Conference year this parcel belongs to"))

	@classmethod
	def parcel_for_sponsoring(cls, sponsoring):
		sponCT = ContentType.objects.get_for_model(Sponsoring)
		return cls.objects.filter(ownerType=sponCT, ownerId=sponsoring.pk)

	def has_read_permission(self, user):
		linked = self.owner
		if linked is not None:
			return linked.has_read_permission(user)
		else:
			return False

	def has_write_permission(self, user):
		linked = self.owner
		if linked is not None:
			return linked.has_write_permission(user)
		else:
			return False
