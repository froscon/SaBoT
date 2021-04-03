from django.views.generic import RedirectView, FormView
from django.contrib.auth import authenticate, login
from django.shortcuts import Http404, redirect
from django.urls import reverse
from django.contrib.auth.models import User

from django_registration.exceptions import ActivationError
from django_registration.backends.activation.views import ActivationView

from account.forms import UserProfileForm, SetPasswordForm
from account.models import UserProfile
from sabot.views import JobProcessingView
from sponsor.views import id_generator

class GenerateAuthTokenView(JobProcessingView):
	next_view = "auth_user_list"

	def process_job(self):
		try:
			user = User.objects.get(pk=self.kwargs["pk"])
		except User.DoesNotExist:
			raise Http404

		try:
			up = UserProfile.objects.get(user=user)
		except UserProfile.DoesNotExist:
			up = UserProfile(user=user)

		up.authToken = id_generator(24)
		up.save()
		return True

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

class ActivateAndSetPWView(ActivationView, FormView):
	form_class = SetPasswordForm
	template_name = "registration/activate_with_pw.html"
	invalid_template_name = "django_registration/activation_failed.html"


	def get(self, request, *args, **kwargs):
		# check if activation link is ok, otherwise link to invalid

		try:
			username = self.validate_key(kwargs.get("activation_key"))
			return super().get(request, *args, **kwargs)
		except ActivationError:
			return self.response_class(
				request = self.request,
				template = self.invalid_template_name,
				context = {})

	def form_valid(self, form):
		try:
			user = self.activate(**self.kwargs)
			user.set_password(form.cleaned_data["password1"])
			user.save()
			return redirect(reverse("login"))
		except ActivationError as e:
			if e.code == "already_activated":
				return redirect(reverse("login"))
			raise Http404
