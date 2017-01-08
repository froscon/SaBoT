import tarfile

from django.views.generic import FormView, UpdateView, RedirectView, CreateView, TemplateView, ListView, DeleteView, DetailView
from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.detail import SingleObjectMixin
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.db.models import Count, Q

from registration.models import RegistrationProfile

from sabot.forms import ParticipantAddForm
# this is the place for generic views


class ObjectPermCheckGETMixin(object):
	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		if not self.object.has_read_permission(self.request.user) and not request.user.is_staff:
			raise PermissionDenied
		return super(ObjectPermCheckGETMixin, self).get(request, *args, **kwargs)

class ObjectPermCheckPOSTMixin(object):
	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		if not self.object.has_write_permission(self.request.user) and not request.user.is_staff:
			raise PermissionDenied
		return super(ObjectPermCheckPOSTMixin, self).post(request, *args, **kwargs)

class ObjectPermCheckMixin(ObjectPermCheckGETMixin, ObjectPermCheckPOSTMixin):
	pass

class CallableSuccessUrlMixin(object):
	def get_success_url(self):
		if callable(self.success_url):
			return self.success_url(self.object, self.kwargs)
		else:
			return super(CallableSuccessUrlMixin, self).get_success_url()

class ChangeNotificationMixin(object):
	def form_valid(self, form):
		changed_fields = form.changed_data
		result = super(ChangeNotificationMixin, self).form_valid(form)

		self.change_notification(changed_fields)
		return result

#		def change_notification(self, changed_fields):

class ParticipantsView(ObjectPermCheckMixin,FormView):
	connection_table_class = None
	object_class = None
	form_class = ParticipantAddForm

	def get_context_data(self, **kwargs):
		kwargs = super(ParticipantsView, self).get_context_data(**kwargs)
		if self.connection_table_class is None:
			raise ImproperlyConfigured("You have to set the connection table class")
		kwargs["participants_list"] = self.connection_table_class.objects.select_related().filter(project=self.object).order_by("user__last_name")
		kwargs["project"] = self.object
		kwargs["object"] = self.object
		kwargs["readonly"] = not self.object.has_write_permission(self.request.user) and not self.request.user.is_staff
		return kwargs

	def get_object(self):
		pk = self.kwargs.get("pk", None)
		if pk is None:
			raise ImproperlyConfigured("You have to pass a pk to ParticipantListView")
		try:
			object = self.object_class.objects.get(pk=pk)
		except self.object_class.DoesNotExist:
			raise Http404
		return object

	def form_valid(self, form):
		email = form.cleaned_data["email"]
		# look for user with this mail
		try:
			try:
				user = User.objects.get(email__iexact=email)
			except User.MultipleObjectsReturned:
				user = User.objects.annotate(profiles=Count("legacy_profile")).get(email__iexact=email,profiles=0)
			# just store the user in the connection table
			# check if this user is already connected
			res = self.connection_table_class.objects.filter(project=self.object,user=user).count()
			if res == 0:
				connection = self.connection_table_class(project=self.object,user=user)
				connection.save()

		except User.DoesNotExist:
			# we create a matching user with emailaddr=username
			site = Site.objects.get_current()

			# we should come up with a unique username
			proposedname = email.split("@")[0]
			if len(proposedname) > 28:
				proposedname = proposedname[:28]

			if len(User.objects.filter(username__iexact=proposedname)) > 0:
				for num in xrange(1,101):
					if len(User.objects.filter(username__iexact=proposedname+str(num))) == 0:
						if num == 101:
							raise ValueError("Unable to create a unique username")
						proposedname = proposedname + str(num)
						break

			new_user = RegistrationProfile.objects.create_inactive_user(proposedname, email, "", site, send_email=False)
			new_user.first_name = form.cleaned_data["first_name"]
			new_user.last_name = form.cleaned_data["last_name"]
			new_user.save()

			# add new user - nontheless
			connection = self.connection_table_class(project=self.object,user=new_user)
			connection.save()

			# send out custom email
			self.send_info_email(new_user)

		newForm = (self.get_form_class())()
		return self.render_to_response(self.get_context_data(form=newForm))

	def send_info_email(self, user):
		profile = RegistrationProfile.objects.get(user=user)
		site = Site.objects.get_current()

		ctx_dict = {'activation_key': profile.activation_key,
			'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
			'site': site,
			'project' : self.object,
			'user' : user}
		subject = render_to_string('registration/activation_email_autocreate_subject.txt', ctx_dict)
		# Email subject *must not* contain newlines
		subject = ''.join(subject.splitlines())

		message = render_to_string('registration/activation_email_autocreate.txt', ctx_dict)

		user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

class ObjectBasedRedirectMixin(object):
	redirect = None
	next_view = None

	def get_redirect_url(self):
		if self.next_view is not None:
			return reverse(self.next_view)
		if self.redirect is None:
			raise ImproperlyConfigured("You have to specify either 'next_view' or 'redirect'")

		if callable(self.redirect):
			return self.redirect(self.object, self.kwargs)
		return self.redirect % self.object.__dict__


class PropertySetterView(SingleObjectMixin, ObjectBasedRedirectMixin, View):
	property_name = None
	property_value = None

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.redirect_url = self.get_redirect_url()
		if callable(self.property_value):
			setattr(self.object, self.property_name, self.property_value(request, **kwargs))
		else:
			setattr(self.object, self.property_name, self.property_value)
		self.object.save()
		return HttpResponseRedirect(self.redirect_url)

class PermCheckPropertySetterView(PropertySetterView):
	permission_checker = lambda obj, user: obj.has_write_permission(user)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		if not self.permission_checker(self.object, self.request.user) and not self.request.user.is_staff:
			raise PermissionDenied

		self.redirect_url = self.get_redirect_url()
		if callable(self.property_value):
			setattr(self.object, self.property_name, self.property_value(request, **kwargs))
		else:
			setattr(self.object, self.property_name, self.property_value)
		self.object.save()
		return HttpResponseRedirect(self.redirect_url)

class PermCheckSimpleDeleteView(SingleObjectMixin, ObjectBasedRedirectMixin, View):
	permission_checker = lambda obj, user: obj.has_write_permission(user)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		if not self.permission_checker(self.object, self.request.user) and not self.request.user.is_staff:
			raise PermissionDenied

		self.redirect_url = self.get_redirect_url()
		self.object.delete()
		return HttpResponseRedirect(self.redirect_url)

	def post(self, request, *args, **kwargs):
		return self.delete(request, *args, **kwargs)



class PermCheckDeleteView(DeleteView, ObjectBasedRedirectMixin):
	permission_checker = staticmethod(lambda obj, user: obj.has_write_permission(user))

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		if not self.permission_checker(self.object, self.request.user) and not self.request.user.is_staff:
			raise PermissionDenied

		self.redirect_url = self.get_redirect_url()
		self.object.delete()
		return HttpResponseRedirect(self.redirect_url)

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		if not self.permission_checker(self.object, self.request.user) and not self.request.user.is_staff:
			raise PermissionDenied
		return super(PermCheckDeleteView, self).get(self, request, *args, **kwargs)


class OwnerSettingCreateView(CreateView):
	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.owner = self.request.user
		self.object.save()
		return redirect(self.get_success_url())

class PermCheckUpdateView(ObjectPermCheckMixin,CallableSuccessUrlMixin,UpdateView):
	# make the form readonly if its only readable
	def get_form(self, form_class):
		form = super(PermCheckUpdateView, self).get_form(form_class)

		if not self.object.has_write_permission(self.request.user) and not self.request.user.is_staff:
			for field in form.fields.values():
				field.widget.attrs["readonly"] = "readonly"
			if hasattr(form,"helper"):
				form.helper.inputs = []
		return form

class PermCheckDetailView(ObjectPermCheckGETMixin, DetailView):
	pass


class EmailOutputView(TemplateView):
	queryset = None

	def get_queryset(self):
		if self.queryset is not None:
			queryset = self.queryset
			if hasattr(queryset, '_clone'):
				queryset = queryset._clone()
		else:
			raise ImproperlyConfigured("You have to enter a queryset")
		return queryset

	def get_context_data(self, **kwargs):
		context = super(EmailOutputView, self).get_context_data(**kwargs)
		context["emails"] = [ u.email for u in self.get_queryset() ]
		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		return self.render_to_response(context, content_type="text/plain")

class XMLListView(ListView):
	def get(self, request, *args, **kwargs):
		self.object_list = self.get_queryset()
		allow_empty = self.get_allow_empty()
		if not allow_empty and len(self.object_list) == 0:
			raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
						% {'class_name': self.__class__.__name__})
		context = self.get_context_data(object_list=self.object_list)
		return self.render_to_response(context,content_type="application/xml")

class MultipleListView(TemplateView):
	template_params = {}

	def get_context_data(self, **kwargs):
		context = super(MultipleListView, self).get_context_data(**kwargs)
		for key, value in self.template_params.items():
			if callable(value):
				context[key] = value(self.request, self.kwargs)
			else:
				context[key] = value._clone()

		return context

class JobProcessingView(TemplateResponseMixin, View):
	success_url = None
	next_view = None
	redirect = None
	error_template_name = None

	def __init__(self, **kwargs):
		super(JobProcessingView, self).__init__(**kwargs)

		self.job_errors = []

	def get_success_url(self):
		if self.success_url is not None:
			return self.success_url
		if self.next_view is not None:
			return reverse(self.next_view)
		if self.redirect is None:
			raise ImproperlyConfigured("You have to specify either 'next_view' or 'redirect'")

		if callable(self.redirect):
			return self.redirect(self)

	def get_template_names(self):
		if self.error_template_name is not None:
			return [self.error_template_name]
		else:
			return super(JobProcessingView, self).get_template_names()

	def get_context_data(self, **kwargs):
		return {
			'params': kwargs,
			'errors': self.job_errors
		}

	def post(self, request, *args, **kwargs):
		if self.process_job():
			return HttpResponseRedirect(self.get_success_url())
		else: # render error template
			context = self.get_context_data(**kwargs)
			return self.render_to_response(context)


class ArchiveCreatorView(View):
	filename = None
	filelist = None


	def get_filename(self):
		return self.filename

	def process_files(self,tarobj):
		if self.filelist is not None:
			if callable(self.filelist):
				files = self.filelist()
			if isinstance(self.filelist, (list,tuple)):
				files = self.filelist()

			for f in files:
				if isinstance(f, tuple):
					tarobj.add(f[0],f[1])
				else:
					tarobj.add(f)


	def get(self, request, *args, **kwargs):
		response = HttpResponse(content_type="application/x-gtar")
		filename = self.get_filename()
		response["Content-Disposition"] = "attachment; filename=" + filename

		self.tarobj = tarfile.open(fileobj=response, mode='w|bz2')

		self.process_files(self.tarobj)

		self.tarobj.close()
		return response
