from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML
from crispy_forms.bootstrap import (
    FormActions,
    StrictButton,
    TabHolder,
    Tab,
    AppendedText,
    PrependedText,
)

from invoice.models import Invoice, DocumentTemplate


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        exclude = ()

    template = forms.ModelChoiceField(
        queryset=DocumentTemplate.objects.filter(docType="INVOICE"),
        label=_("Template to use for this invoice"),
    )
    dueDate = forms.DateField(
        label=_("Due date"),
        input_formats=["%d.%m.%Y", "%d.%m.%y"],
        widget=forms.DateInput(format="%d.%m.%Y"),
    )

    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        # change the invoice number field so that it isn't required anymore
        self.fields["invoiceNumber"].required = False
        self.fields["invoiceNumber"].label = _(
            "Invoice number (leave empty to auto-generate one)"
        )

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("invoiceNumber"),
            Field("dueDate"),
            Field("template"),
        )
        self.helper.add_input(Submit("Create invoice", "Create invoice"))


class OfferForm(forms.Form):
    template = forms.ModelChoiceField(
        queryset=DocumentTemplate.objects.filter(docType="OFFER"),
        label=_("Template to use for this offer"),
    )
