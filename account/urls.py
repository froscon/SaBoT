from django.conf.urls import include, url
from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Sum

from registration.backends.model_activation.views import RegistrationView

from sabot.views import ParticipantsView, OwnerSettingCreateView, PermCheckUpdateView, EmailOutputView, XMLListView, MultipleListView, PropertySetterView, PermCheckPropertySetterView, PermCheckSimpleDeleteView, ArchiveCreatorView
from sabot.decorators import user_is_staff

from account.views import TokenLoginView, UserProfileView, ActivateAndSetPWView
from account.forms import RegistrationFormNameAndUniqueEmail


urlpatterns = [
	url(r'^token/(?P<token>[0-9a-z]+)$', TokenLoginView.as_view(), name="auth_token"),
	url(r'^profile$', login_required(UserProfileView.as_view()), name="auth_user_profile"),
	url(r'^activatepw/(?P<activation_key>\w+)/$', ActivateAndSetPWView.as_view(), name="auth_activate_pw"),
	url(r'^register/?$', RegistrationView.as_view(
							form_class=RegistrationFormNameAndUniqueEmail),
						name = "auth_register_with_name"),
	# staff pages
	url(r'^list+projects/?$',
		user_is_staff(ListView.as_view(
			model = User,
			template_name = "registration/userAffiliation.html")),
		name = "auth_user_affil"),
	url(r'^list/?$',
		user_is_staff(ListView.as_view(
			model = User,
			template_name = "registration/userList.html")),
		name = "auth_user_list"),
	url(r'^(?P<pk>\d+)/makestaff$',
		user_is_staff(PropertySetterView.as_view(
			model = User,
			property_name = "is_staff",
			property_value = True,
			next_view = "auth_user_list")),
		name = "auth_user_makestaff"),
	url(r'^(?P<pk>\d+)/revokestaff$',
		user_is_staff(PropertySetterView.as_view(
			model = User,
			property_name = "is_staff",
			property_value = False,
			next_view = "auth_user_list")),
		name = "auth_user_revokestaff"),
	url(r'^(?P<pk>\d+)/enable$',
		user_is_staff(PropertySetterView.as_view(
			model = User,
			property_name = "is_active",
			property_value = True,
			next_view = "auth_user_list")),
		name = "auth_user_enable"),
	url(r'^(?P<pk>\d+)/disable$',
		user_is_staff(PropertySetterView.as_view(
			model = User,
			property_name = "is_active",
			property_value = False,
			next_view = "auth_user_list")),
		name = "auth_user_disable"),
	url(r'^(?P<pk>\d+)/delete$',
		user_is_staff(DeleteView.as_view(
			model = User,
			template_name = "registration/del.html",
			success_url = "/accounts/list")),
		name = "auth_user_delete"),
	url('^', include('django.contrib.auth.urls')),
]
