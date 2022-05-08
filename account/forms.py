from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


from django_registration.forms import RegistrationFormUniqueEmail
from captcha.fields import ReCaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML


class RegistrationFormNameAndUniqueEmail(RegistrationFormUniqueEmail):
    class Meta(RegistrationFormUniqueEmail.Meta):
        fields = [
            User.USERNAME_FIELD,
            User.get_email_field_name(),
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]
        required_css_class = "required"

    captcha = ReCaptchaField()


class UserProfileForm(forms.Form):
    firstName = forms.CharField(max_length=64, label=_("First name"))
    lastName = forms.CharField(max_length=64, label=_("Last name"))
    email = forms.EmailField(max_length=75, label=_("E-mail"))

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("Save", "Save"))


class SetPasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput, label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput, label=_("Password (again)"))

    def clean(self):
        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Set password"))
