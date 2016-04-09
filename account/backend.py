import models
from django.contrib.auth.models import User

class TokenAuthenticationBackend(object):
	supports_inactive_user = False

	def authenticate(self, token=None):
		try:
			profile = models.UserProfile.objects.get(authToken__iexact=token)
			return profile.user
		except models.UserProfile.DoesNotExist:
			return None


	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None

