from django.template import loader, TemplateDoesNotExist
from events.models import *
from events.middlewares import get_current_request


class DatabaseLoader(loader.base.Loader):
    is_usable = True

    def load_template_source(self, template_name, template_dirs=None):
        try:
            request = get_current_request()
            return Template.objects.get(slug=template_name, owner__groups__in=request.user.groups.all()).template_body, template_name
        except Template.DoesNotExist:
            raise TemplateDoesNotExist(template_name)
