from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML

from exhibitor.models import Exhibitor

class ExhibitorGeneralForm(forms.ModelForm):
	class Meta:
		model = Exhibitor
		fields = ("projectName", "logo", "homepage")

		widgets = {
			"logo" : forms.widgets.FileInput,
		}

	def __init__(self, *args, **kwargs):
		super(ExhibitorGeneralForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		if self.instance and self.instance.logo:
			self.helper.layout = Layout(
				Field("projectName"),
				Field("logo"),
				Div(
					HTML("<p>Current logo:</p><img src=\"{{object.logo.url}}\" style=\"max-height:200px\"/>"),
					css_class = "control-group"),
				Field("homepage"),
#				FormActions(Submit("Save", "Save changes"))
			)
		else:
			self.helper.layout = Layout(
				Field("projectName"),
				Div(
					Div(Field("logo"),css_class = "col-md-2"),
					css_class = "row"
				),
				Field("homepage"),
#				FormActions(Submit("Save", "{% if object %}Save changes{% else %}Register{% endif %}"))
			)

		if self.instance is not None and self.instance.id is not None:
			self.helper.add_input(Submit("Save", "Save changes"))
		else:
			self.helper.add_input(Submit("Save", "Register"))

class ExhibitorDescriptionForm(forms.ModelForm):
	class Meta:
		model = Exhibitor
		fields = ("descriptionDE", "descriptionEN")

	def __init__(self, *args, **kwargs):
		super(ExhibitorDescriptionForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Field("descriptionDE"),
			Field("descriptionEN"),
#			FormActions(Submit("Save", "Save changes"))
		)
		self.helper.add_input(Submit("Save","Save changes"))

class ExhibitorBoothForm(forms.ModelForm):
	class Meta:
		model = Exhibitor
		fields = ("boothPreferedLocation", "boothNumTables", "boothNumChairs", "boothComment")

	def __init__(self, *args, **kwargs):
		super(ExhibitorBoothForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Field("boothPreferedLocation"),
			Field("boothNumTables"),
			Field("boothNumChairs"),
			Field("boothComment"),
#			FormActions(Submit("Save", "Save changes"))
		)
		self.helper.add_input(Submit("Save","Save changes"))
