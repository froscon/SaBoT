# coding: utf8
from django import forms
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML, Hidden
from crispy_forms.bootstrap import (
    FormActions,
    StrictButton,
    TabHolder,
    Tab,
    AppendedText,
    PrependedText,
)

from parcel.models import Parcel
from sponsor.models import Sponsoring


class ParcelAdminForm(forms.ModelForm):
    class Meta:
        model = Parcel
        fields = [
            "ownerType",
            "ownerId",
            "originText",
            "parcelService",
            "trackingUrl",
            "trackingNumber",
            "contentAndUsage",
            "received",
            "storageLocation",
        ]

    ownerAC = forms.CharField(label=_("Project/Sponsor"))

    def __init__(self, *args, **kwargs):
        # initialize ownerAC with correct name if owner is bound
        if "instance" in kwargs and kwargs["instance"] is not None:
            o = kwargs["instance"].owner
            if o:
                if isinstance(o, Sponsoring):
                    name = o.contact.companyName
                else:
                    name = o.projectName
                kwargs["initial"]["ownerAC"] = name
            else:
                kwargs["initial"]["ownerAC"] = kwargs["instance"].originText

        super(ParcelAdminForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("ownerAC"),
            Field("ownerType", type="hidden"),
            Field("ownerId", type="hidden"),
            Field("originText", type="hidden"),
            Field("parcelService"),
            Field("trackingNumber"),
            Field("trackingUrl"),
            Field("contentAndUsage"),
            Field("received"),
            Field("storageLocation"),
        )
        self.helper.add_input(Submit("Save", "Save"))

    def clean(self):
        cleaned_data = super(ParcelAdminForm, self).clean()
        # if a link to the owner is set, remove custom origin text
        if (
            "ownerType" in cleaned_data
            and "ownerId" in cleaned_data
            and cleaned_data["ownerType"] is not None
            and cleaned_data["ownerId"] is not None
        ):
            cleaned_data["originText"] = ""
        return cleaned_data


class UserParcelForm(forms.ModelForm):
    class Meta:
        model = Parcel
        fields = ("parcelService", "trackingUrl", "trackingNumber", "contentAndUsage")

    def __init__(self, *args, **kwargs):
        super(UserParcelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("parcelService"),
            Field("trackingNumber"),
            Field("trackingUrl"),
            Field("contentAndUsage"),
        )
        self.helper.add_input(Submit("Save", "Save"))
