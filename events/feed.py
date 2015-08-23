from datetime import datetime
from django_ical.views import ICalFeed
from events.models import Event


class EventFeed(ICalFeed):
    timezone = 'UTC'
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
        return item.agenda

    def item_start_datetime(self, item):
        if item.when_time:
            return datetime.combine(item.when, item.when_time)
        return item.when
