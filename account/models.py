from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name="legacy_profile", on_delete=models.CASCADE)
	authToken = models.CharField(max_length=64, null=True)

