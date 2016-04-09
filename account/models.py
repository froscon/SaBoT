from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name="legacy_profile")
	authToken = models.CharField(max_length=64, null=True)

