import datetime
import json
import random
import string
from pathlib import Path

from django.conf import settings

from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.core.mail import send_mail
from django.urls import reverse
from django.db import transaction
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import redirect
from django.template import TemplateSyntaxError, TemplateDoesNotExist
from django.template.loader import render_to_string
from django.views.generic.base import TemplateResponseMixin, TemplateView
from django.views.decorators.http import require_POST
from django.views.generic import FormView, CreateView


from account.models import UserProfile
from sabot.multiYear import getActiveYear
from sabot.rt import SabotRtException, SabotRtWrapper, Attachment, TicketStatus
from sabot.views import ChangeNotificationMixin, PermCheckUpdateView, JobProcessingView
from sponsor.forms import (
    SponsorCreationForm,
    SponsorForm,
    SponsorMailSelectorForm,
    PackagesImporterForm,
)
from sponsor.models import Sponsoring, SponsorContact, SponsorPackage


def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for x in range(size))


class SponsorEmailingView(FormView):
    form_class = SponsorMailSelectorForm
    template_name = "sponsor/contactMailer/mailform.html"
    success_template_name = "sponsor/contactMailer/mailformResults.html"

    def get_context_data(self, **kwargs):
        kwargs = super(SponsorEmailingView, self).get_context_data(**kwargs)
        kwargs["contact_list"] = SponsorContact.objects.select_related()
        return kwargs

    def form_valid(self, form):
        results = []
        rt = SabotRtWrapper()
        for contact in form.cleaned_data["recipients"]:
            result = {}
            result["contact"] = contact

            # now compose the mail and send it via RT
            tmpl = contact.template
            ctx_dict = {"rcpt": contact}
            try:
                message = render_to_string(tmpl.template.templateName, ctx_dict)
            except TemplateSyntaxError as e:
                result["info"] = "Template syntax error: {}".format(e)
                result["status"] = "failed"
                results.append(result)
                continue
            except TemplateDoesNotExist as e:
                result["info"] = "Template not found: {}".format(e)
                result["status"] = "failed"
                results.append(result)
                continue
            requestor = (
                (
                    contact.contactPersonEmail
                    if len(contact.contactPersonEmail) > 0
                    else contact.contactEMail
                ),
            )

            # handle attachments
            attachments = [
                Attachment(att.name, Path(att.attachment.path))
                for att in tmpl.attachments.all()
            ]
            # post it to rt
            try:
                ticket_id = rt.create_ticket(
                    queue=settings.RT_QUEUE,
                    owner=settings.RT_TICKET_OWNER,
                    subject=contact.template.mailSubject,
                    requestor=requestor,
                    text=message,
                    status=TicketStatus.OPEN,
                    attachments=attachments,
                    send_mail=True,
                )
                rt.update_status(ticket_id, TicketStatus.STALLED)
            except SabotRtException as e:
                result["status"] = "failed"
                result["info"] = str(e)
                results.append(result)
                continue

            result["status"] = "ok"
            results.append(result)
            contact.lastMailed = datetime.date.today()
            contact.rtTicketId = ticket_id
            contact.save()

        self.template_name = self.success_template_name
        return self.render_to_response(self.get_context_data(results=results))


def sponsorMailPreview(request, pk):
    resp = {}
    resp["success"] = False
    try:
        contact = SponsorContact.objects.get(pk=pk)
        resp["company"] = contact.companyName
        tmpl = contact.template
        if tmpl is not None:
            ctx_dict = {"rcpt": contact}
            try:
                message = render_to_string(tmpl.template.templateName, ctx_dict)
                resp["message"] = message
                names = []
                if len(tmpl.attachments.all()) > 0:
                    names = [att.name for att in tmpl.attachments.all()]

                resp["attachments"] = names

                resp["success"] = True
            except TemplateSyntaxError as e:
                resp["errormsg"] = "Template syntax error: {}".format(e)
            except TemplateDoesNotExist as e:
                resp["errormsg"] = "Template not found: {}".format(e)

    except SponsorContact.DoesNotExist:
        pass

    return HttpResponse(json.dumps(resp), content_type="application/json")


class SponsorCreateView(FormView):
    form_class = SponsorCreationForm
    template_name = "sponsor/sponsoring/create.html"
    success_url = "../{id}"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["year"] = getActiveYear(self.request)
        return kwargs

    def form_valid(self, form):
        # create a new user for this sponsor
        try:
            sp = transaction.savepoint()
            baseContact = form.cleaned_data["sponsorContact"]

            try:
                user = User.objects.get(username=form.cleaned_data["sponsorUsername"])
            except User.DoesNotExist:
                user = User(username=form.cleaned_data["sponsorUsername"])
                user.first_name = baseContact.contactPersonFirstname
                user.last_name = baseContact.contactPersonSurname
                user.email = baseContact.contactPersonEmail
                user.save()

                profile = UserProfile(user=user)
                profile.authToken = id_generator(24)
                profile.save()

            sponsoring = Sponsoring()
            sponsoring.owner = user
            sponsoring.year = getActiveYear(self.request)
            sponsoring.contact = baseContact
            sponsoring.package = form.cleaned_data["sponsorPackage"]
            sponsoring.adminComment = form.cleaned_data["internalComment"]
            sponsoring.save()

            self.object = sponsoring

            transaction.savepoint_commit(sp)
        except Exception as e:
            transaction.savepoint_rollback(sp)
            raise e

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(SponsorCreateView, self).get_context_data(**kwargs)
        try:
            sponsorContact = SponsorContact.objects.get(pk=self.kwargs["pk"])
        except SponsorContact.DoesNotExist:
            raise Http404
        context["sponsorContact"] = sponsorContact
        return context

    def get_success_url(self):
        if self.success_url:
            url = self.success_url.format(**self.object.__dict__)
        else:
            raise ImproperlyConfigured("No URL to redirect to")
        return url


class PackagesImporterView(FormView):
    form_class = PackagesImporterForm
    success_url = "./list"

    @transaction.atomic
    def form_valid(self, form):
        currentYear = getActiveYear(self.request)
        selectedYear = form.cleaned_data["fromYear"].year
        packagesToBeImported = SponsorPackage.objects.filter(year=selectedYear)

        for package in packagesToBeImported:
            # The django way of copying a model is to set pk=None o_O
            package.pk = None
            package.year = currentYear
            package.save()

        return redirect(self.success_url)

    def form_invalid(self, form):
        return redirect(self.success_url)


class SponsorUpdateView(ChangeNotificationMixin, PermCheckUpdateView):
    model = Sponsoring
    form_class = SponsorForm
    template_name = "sponsor/sponsoring/update.html"

    def get_context_data(self, **kwargs):
        kwargs["object"] = self.object
        return super(SponsorUpdateView, self).get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super(SponsorUpdateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_success_url(self):
        return reverse("sponsor_update", kwargs={"pk": self.object.pk})

    def change_notification(self, changed_fields):
        if len(changed_fields) == 0:
            return
        change_dict = {}
        for field in changed_fields:
            field_name = self.object.fieldDescriptionalNames.get(field, field)
            change_dict[field_name] = getattr(self.object, field)

        ctx_dict = {
            "sponsor": self.object,
            "change_dict": change_dict,
            "user": self.request.user,
        }
        subject = "Sponsor information change notification"
        message = render_to_string("sponsor/change_notification_email.txt", ctx_dict)
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            settings.SPONSOR_NOTIFICATION,
            fail_silently=True,
        )

        if (
            "clearedForBilling" in changed_fields
            and self.object.clearedForBilling == True
        ):
            subject = "Sponsoring ready for billing"
            message = render_to_string(
                "sponsor/ready_for_billing_notification_email.txt", ctx_dict
            )
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                settings.FINANCE_EMAIL,
                fail_silently=True,
            )


class SponsorContactResetEmailView(JobProcessingView, TemplateView):
    def process_job(self):
        SponsorContact.objects.all().update(
            responded=False, lastMailed=None, rtTicketId=None
        )
        return True


def respond_json(jdata):
    return HttpResponse(json.dumps(jdata), content_type="application/json")


@require_POST
def loadResponseInfoFromRT(request):
    res = {"failed": 0, "succeded": 0, "updated": 0}

    unansweredContacts = SponsorContact.objects.filter(responded=False).exclude(
        rtTicketId=None
    )
    rt = SabotRtWrapper()
    for contact in unansweredContacts:
        if rt.check_correspondance(contact.rtTicketId):
            res["updated"] = res["updated"] + 1
            contact.responded = True
            contact.save()
        res["succeded"] = res["succeded"] + 1

    return respond_json(res)
