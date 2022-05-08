import json
from datetime import date
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.urls import reverse
from django.http import (
    Http404,
    HttpResponseNotAllowed,
    HttpResponse,
    HttpResponseRedirect,
)
from django.template.loader import render_to_string
from django.views.generic import UpdateView

from sabot.rt import SabotRtException, SabotRtWrapper, Attachment
from sabot.views import JobProcessingView
from invoice.forms import InvoiceForm
from invoice.models import (
    DocumentTemplate,
    Invoice,
    SMSKaufenSnailMailJob,
    YearlyInvoiceCounters,
)
from invoice import odtemplate
from sponsor.models import Sponsoring


import smskaufen.api


def respond_json(jdata):
    return HttpResponse(json.dumps(jdata), content_type="application/json")


class InvoiceCreateUpdateView(UpdateView):
    form_class = InvoiceForm
    model = Invoice
    template_name = "invoice/create_update_invoice.html"
    next_view = None

    # This view obtains in parameter "spk" the sponsoring. In order to
    # retrieve a potential invoice. If there is none, return None to not
    # bind this form.
    def get_object(self):
        try:
            self.sponsoring = Sponsoring.objects.get(pk=self.kwargs["spk"])
        except Sponsoring.DoesNotExist:
            # if there is no matching Sponsoring, we don't do anything
            raise Http404
        object = None
        try:
            object = self.sponsoring.invoice
        except Invoice.DoesNotExist:
            pass
        return object

    def get_context_data(self, **kwargs):
        # Additionally inject the sponsoring to the template
        kwargs["sponsoring"] = self.sponsoring
        kwargs["object"] = self.object
        return super(InvoiceCreateUpdateView, self).get_context_data(**kwargs)

    def get_initial(self):
        # if there is no invoice already present, prepopulate the invoice number
        if self.object is None:
            return {
                "dueDate": date.today() + settings.INVOICE_DEFAULT_PAYMENT_TIME,
            }
        else:
            return {}

    def form_valid(self, form):
        invoice = form.save(commit=False)

        # fill in sponsoring
        invoice.sponsoring = self.sponsoring
        invoice.invoiceAmount = self.sponsoring.package.price
        # check if we should auto generate an invoice Number
        # WARNING: I know that this has the potential for race conditions, however
        # I ignore this here. This is a potential FIXME
        if invoice.invoiceNumber == "":
            cntr = YearlyInvoiceCounters.get_next_counter()
            invoice.invoiceNumber = settings.INVOICE_NUMBER_FORMAT.format(
                year=date.today().year, cntr=cntr
            )
            YearlyInvoiceCounters.update_counter(cntr)

        invoice.save()
        # generate pdf
        try:
            invoice.render_pdf()
        except Invoice.PDFRenderingError:
            pass

        return HttpResponseRedirect(reverse(self.next_view))


def SMSKaufenStatusUpdate(request, invId):
    try:
        invoice = Invoice.objects.get(invoiceNumber=invId)
    except Invoice.DoesNotExist:
        raise Http404

    smj = invoice.sponsoring.snailmailinvoice
    if smj is None:
        raise Http404

    if "statustext" not in request.GET or "auftrag" not in request.GET:
        smj.joberror = "Status update received but incomplete"
        smj.save()
        return HttpResponse("")

    try:
        auftrag = int(request.GET["auftrag"])
    except ValueError:
        smj.joberror = "Status update with non-numeric jobid"
        smj.save()
        return HttpResponse("")

    if auftrag != smj.jobid:
        smj.joberror = "Status update with invalid jobid"
        smj.save()

    statustext = request.GET["statustext"].strip().lower()

    if statustext == "ok":
        smj.success = True
        smj.save()
        return HttpResponse("")
    else:
        smj.joberror = statustext
        smj.save()
        return HttpResponse("")


def InvoiceEmailTemplate(request, spk):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    res = {}
    res["status"] = "unknown"

    try:
        sponsoring = Sponsoring.objects.select_related("invoice").get(pk=spk)
    except Sponsoring.DoesNotExist:
        res["status"] = "error"
        res["errmsg"] = "Cannot find sponsoring for given id"
        return respond_json(res)

    templateName = (
        "invoice/mail/invoiceMailDE.html"
        if sponsoring.contact.contactPersonLanguage.startswith("de")
        else "invoice/mail/invoiceMailEN.html"
    )
    ctx_dict = {"sponsoring": sponsoring, "user": request.user}
    message = render_to_string(templateName, ctx_dict)

    res["status"] = "success"
    res["success"] = True
    res["company"] = sponsoring.contact.companyName
    res["message"] = message
    return respond_json(res)


class RTinvoiceView(JobProcessingView):
    next_view = "invoice_overview"
    error_template_name = "invoice/rt_error.html"

    def get_sponsoring(self, sid):
        try:
            sponsoring = Sponsoring.objects.select_related("invoice").get(pk=sid)
        except Sponsoring.DoesNotExist:
            raise Http404
        return sponsoring

    def process_job(self):
        if "text" not in self.request.POST:
            self.job_errors.append("invalid request: item 'text' missing.")
            return False

        sponsoring = self.get_sponsoring(self.kwargs["spk"])

        # check if invoice already exists
        if Invoice.objects.filter(sponsoring=sponsoring).count() > 0:
            invoice = sponsoring.invoice
        else:
            invoice = None
        if invoice is None:
            self.job_errors.append("There is no invoice for this sponsoring.")
            return False
        if not invoice.pdf:
            self.job_errors.append(
                "There is no invoice PDF available for this sponsoring."
            )
            return False

        rt = SabotRtWrapper()
        if sponsoring.contact.contactPersonLanguage.startswith("de"):
            subject = "Rechnung Partner-Paket {} {}".format(
                settings.CONFERENCE_NAME, date.today().year
            )
        else:
            subject = "Invoice Partnership {} {}".format(
                settings.CONFERENCE_NAME, date.today().year
            )

        attachments = [
            Attachment(
                f"{sponsoring.invoice.invoiceNumber}.pdf",
                Path(sponsoring.invoice.pdf.path),
            )
        ]

        try:
            ticket_id = rt.create_ticket(
                queue=settings.RT_QUEUE_INVOICE,
                owner=self.request.user.username,
                subject=subject,
                text=self.request.POST["text"],
                requestor=sponsoring.contact.contactPersonEmail,
                attachments=attachments,
                send_mail=True,
            )
        except SabotRtException as e:
            self.job_errors.append(f"RT Correspondance failed: {e}")
            return False

        invoice.rtTicketRef = ticket_id
        invoice.save()
        return True


class InvoiceSnailMailView(JobProcessingView):
    next_view = "invoice_overview"
    error_template_name = "invoice/error-smskaufen.html"

    def get_sponsoring(self, sid):
        try:
            sponsoring = Sponsoring.objects.select_related(
                "invoice", "snailmailinvoice", "contact"
            ).get(pk=sid)
        except Sponsoring.DoesNotExist:
            raise Http404
        return sponsoring

    def process_job(self):
        self.sponsoring = self.get_sponsoring(self.kwargs["spk"])

        if not self.sponsoring.invoice:
            self.job_errors.append("The given sponsoring has no invoice")
            return False
        elif not self.sponsoring.invoice.pdf:
            self.job_errors.append(
                "There is no invoice PDF available for this sponsoring."
            )
            return False
        if SMSKaufenSnailMailJob.objects.filter(sponsoring=self.sponsoring).count() > 0:
            self.job_errors.append(
                "A snailmail invoice was already created. You should not have reached this view"
            )
            return False

        feedPath = reverse(
            "invoice_snailmailstatus",
            kwargs={"invId": self.sponsoring.invoice.invoiceNumber},
        )
        feedUrl = settings.INSTALL_MAIN_URL + feedPath

        international = self.sponsoring.billingInForeignCountry

        # try to send it out via smskaufen
        try:
            result = smskaufen.api.sendLetter(
                self.sponsoring.invoice.pdf.file,
                color=True,
                feedUrl=feedUrl,
                international=international,
            )
        except smskaufen.api.SmskaufenException as e:
            self.job_errors.append(e.message)
            return False

        s = SMSKaufenSnailMailJob()
        s.sponsoring = self.sponsoring
        s.jobid = result
        s.save()

        return True


def generateSponsoringOfferPDF(request, spk, template):
    return generateSponsoringOffer(request, spk, template, pdf_output=True)


def generateSponsoringOffer(request, spk, template, pdf_output=False):
    try:
        sponsoring = Sponsoring.objects.get(pk=spk)
    except Sponsoring.DoesNotExist:
        raise Http404
    try:
        template = DocumentTemplate.objects.get(pk=template)
    except DocumentTemplate.DoesNotExist:
        raise Http404

    # otherwise, we render it
    contact = sponsoring.contact
    postLines = [
        contact.companyName,
        contact.contactPersonFirstname + " " + contact.contactPersonSurname,
        contact.address2,
        contact.street,
        contact.zipcode + " " + contact.city,
    ]
    postalAddress = "\n".join([l for l in postLines if l != ""])

    context = {
        "POSTAL_ADDRESS": postalAddress,
        "PACKAGE_NAME": sponsoring.package.name,
        "PACKAGE_DESCRIPTION": "\n".join(sponsoring.getPacketDescription()),
        "VAT": str(settings.INVOICE_VAT),
        "PRICE_NET": str(sponsoring.package.price.quantize(Decimal("0.01"))),
        "PRICE_GROSS": str(sponsoring.package.getPriceGross()),
        "VAT_TOTAL": str(sponsoring.package.getVATAmount()),
        "CONTACT_LASTNAME": sponsoring.contact.contactPersonSurname,
        "CONTACT_FIRSRNAME": sponsoring.contact.contactPersonFirstname,
        "COMPANY_NAME": sponsoring.contact.companyName,
    }
    temp = odtemplate.ODTTemplate(template.template.path)
    temp.render(context)
    if pdf_output:
        f = temp.getTemporaryPDF()
        response = HttpResponse(f, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="offer.pdf"'
    else:
        f = open(temp.getTemporaryODT(), "rb")
        response = HttpResponse(
            f, content_type="application/vnd.oasis.opendocument.text"
        )
        response["Content-Disposition"] = 'attachment; filename="offer.odt"'
    return response
