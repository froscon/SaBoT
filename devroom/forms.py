from django import forms
from models import Devroom
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML
from crispy_forms.bootstrap import FormActions, StrictButton, TabHolder, Tab

class DevroomGeneralForm(forms.ModelForm):
	class Meta:
		model = Devroom
		fields = ("projectName", "logo", "homepage")

		widgets = {
			"logo" : forms.widgets.FileInput,
		}

	def __init__(self, *args, **kwargs):
		super(DevroomGeneralForm, self).__init__(*args, **kwargs)
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


class DevroomDescriptionForm(forms.ModelForm):
	class Meta:
		model = Devroom
		fields = ("descriptionDE", "descriptionEN")

	def __init__(self, *args, **kwargs):
		super(DevroomDescriptionForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Field("descriptionDE"),
			Field("descriptionEN"),
#			FormActions(Submit("Save", "Save changes"))
		)
		self.helper.add_input(Submit("Save","Save changes"))

class DevroomProgramForm(forms.ModelForm):
	class Meta:
		model = Devroom
		fields = ("schedule", "plannedProgram", "anticipatedGuests")

		widgets = {
			"schedule" : forms.widgets.Textarea(attrs={"rows" : 3 })
		}

	def __init__(self, *args, **kwargs):
		super(DevroomProgramForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Field("schedule"),
			Field("plannedProgram"),
			Field("anticipatedGuests"),
#			FormActions(Submit("Save", "Save changes"))
		)
		self.helper.add_input(Submit("Save","Save changes"))

class DevroomSetRoomForm(forms.Form):
	room = forms.CharField(max_length=16, required=False)

