from django.shortcuts import render_to_response, redirect
from django.template import Context
from django.template.loader import get_template
from events.models import Template, Preview

import mailchimp


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


def get_mailchimp_api():
    return mailchimp.Mailchimp('00000000000000000000000000000000-us1')


# def campaign():
#     mc = get_mailchimp_api()
#     mc.campaigns.create("regular", )
