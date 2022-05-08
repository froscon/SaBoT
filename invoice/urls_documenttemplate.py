from django.urls import path
from django.views.generic import ListView, DeleteView, CreateView, UpdateView

from sabot.decorators import user_is_staff
from invoice.models import DocumentTemplate

urlpatterns = [
    path(
        "new",
        user_is_staff(
            CreateView.as_view(
                model=DocumentTemplate,
                fields=[
                    "description",
                    "template",
                    "docType",
                ],
                template_name="invoice/documenttemplate/update.html",
                success_url="./{id}",
            )
        ),
        name="documenttemplate_new",
    ),
    path(
        "<int:pk>",
        user_is_staff(
            UpdateView.as_view(
                model=DocumentTemplate,
                fields=[
                    "description",
                    "template",
                    "docType",
                ],
                template_name="invoice/documenttemplate/update.html",
                success_url="./{id}",
            )
        ),
        name="documenttemplate_update",
    ),
    path(
        "list",
        user_is_staff(
            ListView.as_view(
                queryset=DocumentTemplate.objects.all(),
                template_name="invoice/documenttemplate/list.html",
            )
        ),
        name="documenttemplate_list",
    ),
    path(
        "del/<int:pk>",
        user_is_staff(
            DeleteView.as_view(
                model=DocumentTemplate,
                template_name="invoice/documenttemplate/del.html",
                success_url="../list",
            )
        ),
        name="documenttemplate_del",
    ),
]
