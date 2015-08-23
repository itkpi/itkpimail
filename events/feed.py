from datetime import datetime
from django_ical.views import ICalFeed
import re
from events.models import Event


class EventFeed(ICalFeed):
    timezone = 'EET'
    file_name = "events.ics"

    def get_feed(self, obj, request):
        self.request = request
        return super().get_feed(obj, request)

    def product_id(self):
        return '-//{}//Events//UK'.format(self.request.get_host())

    def items(self):
        return Event.objects.all().order_by('-when')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        agenda = item.agenda
        agenda = re.sub(r'<p[^>]*>', '\n', agenda)
        agenda = re.sub(r'<br[^>]*>', '\n', agenda)
        agenda = re.sub(r'<[^>]*>', '', agenda)
        return agenda.strip()

    def item_start_datetime(self, item):
        if item.when_time:
            return datetime.combine(item.when, item.when_time)
        return item.when

    def item_end_datetime(self, item):
        if item.when_end:
            if item.when_end_time:
                return datetime.combine(item.when_end, item.when_end_time)
            return item.when_end

    def item_location(self, item):
        return item.place
