from django.shortcuts import render_to_response, redirect
from django.template import Context
from django.template.loader import get_template
from events.models import Template, Preview


def generate_mail(modeladmin, request, queryset):
    template_id = request.POST['template']
    template_db = Template.objects.get(pk=int(template_id))
    template_slug = template_db.slug
    template = get_template(template_slug)
    rendered = template.render(Context({"events": queryset.order_by('date')}))

    preview = Preview(template=template_db, body=str(rendered))
    preview.save()
    return redirect(preview)  # render_to_response("preview.html", {"preview": p})

generate_mail.short_description = "Сгенерировать письмо"
