# coding: utf8
from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML, Hidden
from crispy_forms.bootstrap import FormActions, StrictButton, TabHolder, Tab, AppendedText, PrependedText

from parcel.models import Parcel
from sponsor.models import Sponsoring

class ParcelAdminForm(forms.ModelForm):
	class Meta:
		model = Parcel
		fields = ("ownerType", "ownerId", "parcelService", "trackingUrl", "trackingNumber", "contentAndUsage", "received", "storageLocation")

	ownerAC = forms.CharField(label=_("Project/Sponsor"))

	def __init__(self, *args, **kwargs):
		# initialize ownerAC with correct name if owner is bound
		if "instance" in kwargs:
			o = kwargs["instance"].owner
			if o:
				if isinstance(o, Sponsoring):
					name = o.contact.companyName
				else:
					name = o.projectName
				kwargs["initial"]["ownerAC"] = name

		super(ParcelAdminForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Field("ownerAC"),
			Field("ownerType", type="hidden"),
			Field("ownerId", type="hidden"),
			Field("parcelService"),
			Field("trackingNumber"),
			Field("trackingUrl"),
			Field("contentAndUsage"),
			Field("received"),
			Field("storageLocation"),
		)
		self.helper.add_input(Submit("Save", "Save"))
