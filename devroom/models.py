from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class Devroom(models.Model):
	owner = models.ForeignKey(User,editable=False,related_name="devrooms")
	createDate = models.DateField(auto_now_add=True,editable=False)
	modifyDate = models.DateField(auto_now=True, editable=False)
	projectName = models.CharField(max_length=128, verbose_name=_("Project name"))
	logo = models.ImageField(blank=True,upload_to="devrooms/logos", verbose_name=_("Project logo"))
	homepage = models.URLField(blank=True, verbose_name=_("Project homepage url"))

	descriptionDE = models.TextField(blank=True, verbose_name=_("Description text of your project (German)"))
	descriptionEN = models.TextField(blank=True, verbose_name=_("Description text of your project (English)"))

	schedule = models.TextField(blank=True, verbose_name=_("How long do you want to use the dev room? (e.g. one day/both days/only one afternoom) If you don't want the complete time, do you have a preferred day/time?"))
	plannedProgram = models.TextField(blank=True, verbose_name=_("Give a short description of the program you plan for the Devroom. We will choose the projects based on this description. If you have special requirements, please note this also here."))
	anticipatedGuests = models.PositiveIntegerField(blank=True,null=True,verbose_name=_("For how many guests is your programme planned? If you don't plan with a fixed number, how many guests do you expect to have? (We use this to plan the room sizes)"))

	participants = models.ManyToManyField(User,blank=True,editable=False,related_name="devroomparticipation+", through="DevroomParticipants")

	accepted = models.BooleanField(default=False, editable=False)
	room = models.CharField(max_length=16,editable=False,blank=True)

	year = models.PositiveIntegerField(editable=False, verbose_name=_("Conference year this devroom belongs to"))

	def has_read_permission(self, user):
		return DevroomParticipants.objects.filter(user=user).count() > 0 or user == self.owner

	def has_write_permission(self, user):
		return DevroomParticipants.objects.filter(user=user,isAdmin=True).count() > 0 or user == self.owner

class DevroomParticipants(models.Model):
	project = models.ForeignKey(Devroom)
	user = models.ForeignKey(User)
	isAdmin = models.BooleanField(default=False)
