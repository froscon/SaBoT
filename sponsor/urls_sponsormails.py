from django.urls import path
from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from sponsor.models import SponsorMail
from sabot.decorators import user_is_staff

urlpatterns = [
    path(
        "new",
        user_is_staff(
            CreateView.as_view(
                model=SponsorMail,
                fields=[
                    "mailTemplateName",
                    "template",
                    "mailSubject",
                    "attachments",
                ],
                template_name="sponsor/mail/update.html",
                success_url="list",
            )
        ),
        name="sponsormail_new",
    ),
    path(
        "<int:pk>",
        user_is_staff(
            UpdateView.as_view(
                model=SponsorMail,
                fields=[
                    "mailTemplateName",
                    "template",
                    "mailSubject",
                    "attachments",
                ],
                template_name="sponsor/mail/update.html",
                success_url="list",
            )
        ),
        name="sponsormail_update",
    ),
    path(
        "list",
        user_is_staff(
            ListView.as_view(
                queryset=SponsorMail.objects.all(),
                template_name="sponsor/mail/list.html",
            )
        ),
        name="sponsormail_list",
    ),
    path(
        "del/<int:pk>",
        user_is_staff(
            DeleteView.as_view(
                model=SponsorMail,
                template_name="sponsor/mail/del.html",
                success_url="../list",
            )
        ),
        name="sponsormail_del",
    ),
]
