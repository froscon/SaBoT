from django import forms


class ParticipantAddForm(forms.Form):
    required_css_class = "form-control"  # this is bootstrap3 element class

    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=128)
