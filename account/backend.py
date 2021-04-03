import models
from django.contrib.auth.models import User


class TokenAuthenticationBackend(object):
    supports_inactive_user = False

    def authenticate(self, token=None):
        if token is None or len(token) == 0:
            return None
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


class APITokenMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            token = request.META.get("HTTP_TOKEN")
            if token is not None:
                profile = models.UserProfile.objects.get(authToken__iexact=token)
                request.user = profile.user
        except models.UserProfile.DoesNotExist:
            pass
        return self.get_response(request)
