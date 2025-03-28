from django.conf import settings

from crispy_forms.bootstrap import Tab
from crispy_forms.layout import Field
from crispy_forms.utils import render_field

TEMPLATE_PACK = getattr(settings, "CRISPY_TEMPLATE_PACK", "bootstrap")


class TextOptOut(Field):
    template = "crispy_extensions/text_optout.html"

    def __init__(self, field, *args, **kwargs):
        self.field = field

        super(TextOptOut, self).__init__(field, *args, **kwargs)

    def render(self, form, context, template_pack=TEMPLATE_PACK, extra_context=None, **kwargs):
        template = self.get_template_name(template_pack)
        return render_field(
            self.field,
            form,
            context,
            template=template,
            attrs=self.attrs,
            template_pack=template_pack,
            extra_context=extra_context,
            **kwargs
        ) + render_field(
            self.field + "OptOut",
            form,
            context,
            template=template,
            attrs={"type": "hidden"},
            template_pack=template_pack,
        )
