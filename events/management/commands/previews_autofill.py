from django.core.management.base import BaseCommand
from events.models import Event, Preview
import re


class Command(BaseCommand):
    help = 'Autofill relation between events and previews by parsing preview body'

    def handle(self, *args, **options):
        for preview in Preview.objects.all():
            events_list = re.findall(r"#event(\d+)", preview.body)
            self.stdout.write('Preview {} contains {} events:'.format(preview.pk, events_list))
            for event_id in re.findall(r"#event(\d+)", preview.body):
                e = Event.objects.get(pk=int(event_id))
                e.previews.add(preview)
                e.save()
                self.stdout.write('  - Added {} to {}'.format(preview.pk, event_id))

