from django.template import loader, TemplateDoesNotExist
from events.models import *


class DatabaseLoader(loader.base.Loader):
    is_usable = True

    def load_template_source(self, template_name, template_dirs=None):
        try:
            return Template.objects.get(slug=template_name).template_body, template_name
        except Template.DoesNotExist:
            raise TemplateDoesNotExist(template_name)
