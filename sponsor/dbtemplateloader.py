from django.template import TemplateDoesNotExist, Origin, Template
from django.template.loaders.base import Loader as BaseLoader

from sponsor.models import SponsorMailTemplate


class DBLoader(BaseLoader):
    is_usable = True

    def get_template_sources(self, template_name, template_dirs=None):
        tmpls = SponsorMailTemplate.objects.filter(templateName__exact=template_name)
        for tmpl in tmpls:
            yield Origin(
                name="DBLoader::{}".format(template_name),
                template_name=template_name,
                loader=self,
            )

    def get_contents(self, origin):
        try:
            tmpl = SponsorMailTemplate.objects.get(
                templateName__exact=origin.template_name
            )
            return tmpl.template
        except SponsorMailTemplate.DoesNotExist:
            raise TemplateDoesNotExist(origin)
