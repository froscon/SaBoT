from django.views.generic import RedirectView, FormView
from django.contrib.auth import authenticate, login
from django.shortcuts import Http404, redirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.contrib.auth.models import User

from registration.models import RegistrationProfile
from registration.backends.default.views import RegistrationView

from forms import UserProfileForm, SetPasswordForm
from forms import RegistrationFormNameAndUniqueEmail
from models import UserProfile

class TokenLoginView(RedirectView):
	permanent = False
	def get_redirect_url(self, **kwargs):
		user = authenticate(token = kwargs["token"])
		if user is not None:
			if user.is_active:
				login(self.request, user)
				return self.request.GET.get("next","/")

		raise Http404

class UserProfileView(FormView):
	template_name = "registration/profile.html"
	form_class = UserProfileForm

	def get_initial(self):
		return {
				"firstName" : self.request.user.first_name,
				"lastName" : self.request.user.last_name,
				"email" : self.request.user.email,
			}

	def form_valid(self, form):
		user = self.request.user
		user.first_name = form.cleaned_data["firstName"]
		user.last_name = form.cleaned_data["lastName"]
		user.email = form.cleaned_data["email"]
		user.save()
		return self.form_invalid(form)

class ActivateAndSetPWView(FormView):
	form_class = SetPasswordForm
	template_name = "registration/activate_with_pw.html"
	invalid_template_name = "registration/activate.html"


	def get(self, request, *args, **kwargs):
		# check if activation link is ok, otherwise link to invalid
		try:
			profile = RegistrationProfile.objects.get(activation_key=kwargs["activation_key"])
			return super(ActivateAndSetPWView, self).get(request, *args, **kwargs)
		except RegistrationProfile.DoesNotExist:
			return self.response_class(
				request = self.request,
				template = self.invalid_template_name,
				context = {})

	def form_valid(self, form):
		try:
			profile = RegistrationProfile.objects.get(activation_key=self.kwargs["activation_key"])
			profile.user.set_password(form.cleaned_data["password1"])
			profile.user.save()
			RegistrationProfile.objects.activate_user(self.kwargs["activation_key"])
			return redirect(reverse("auth_login"))
		except RegistrationProfile.DoesNotExist:
			raise Http404
