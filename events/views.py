from django.views.generic import TemplateView
from events.models import Preview


class PreviewView(TemplateView):
    template_name = "preview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        preview = Preview.objects.get(pk=int(kwargs["p_id"]))
        context["preview"] = preview
        return context
