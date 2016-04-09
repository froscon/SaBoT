# Create your views here.
from django.views.generic import FormView
from forms import DevroomSetRoomForm
from django.http import Http404
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.http import HttpResponseRedirect
from models import Devroom

class SetRoomView(FormView):
	form_class = DevroomSetRoomForm

	def form_invalid(self, form):
		raise Http404

	def form_valid(self, form):
		roomId = self.kwargs.get("pk", None)
		if roomId is None:
			raise ImproperlyConfigured("You have to provide a pk for the room")
		try:
			room = Devroom.objects.get(id=roomId)
		except Devroom.DoesNotExist:
			raise Http404

		room.room = form.cleaned_data["room"]
		room.save()
		return HttpResponseRedirect(self.get_success_url())
