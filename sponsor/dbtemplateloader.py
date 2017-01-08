from django.template import TemplateDoesNotExist
from django.template.loaders.base import Loader as BaseLoader

from sponsor.models import SponsorMailTemplate

class DBLoader(BaseLoader):
	is_usable = True
	def load_template(self, template_name, template_dirs=None):
		try:
			tmpl = SponsorMailTemplate.objects.get(templateName__exact=template_name)
			return (tmpl.template, "DBLoader::{}".format(template_name))
		except SponsorMailTemplate.DoesNotExist:
			raise TemplateDoesNotExist(template_name)
