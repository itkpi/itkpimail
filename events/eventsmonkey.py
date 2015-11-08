import dateutil.parser
import requests


class EventsMonkeyAPIError(Exception):
    pass


def date_format(date):
    date = dateutil.parser.parse(date)
    native = date.replace(tzinfo=None)
    return native.strftime('%Y-%m-%d %H:%M')


class EventsMonkey:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def suggest(self, data):
        response = self.session.post(self.suggest_url,
                                     json=data)
        self.process_errors(response)
        data = response.json()
        return data

    def edit(self, secret, data):
        data['secret'] = secret
        response = self.session.put(self.resource_item_url(secret),
                                    json=data)
        self.process_errors(response)
        data = response.json()
        return data

    def get(self, secret):
        response = self.session.get(self.resource_item_url(secret))
        self.process_errors(response)
        data = response.json()
        data['when_start'] = date_format(data['when_start'])
        if data['when_end']:
            data['when_end'] = date_format(data['when_end'])
        return data

    def resource_item_url(self, secret):
        return "{}/{}".format(self.suggest_url, secret)

    @property
    def suggest_url(self):
        return '{}/api/v1/suggested_events'.format(self.url)

    def process_errors(self, response):
        if response.status_code > 299:
            if response.status_code == 400:
                raise EventsMonkeyAPIError('EventsMonkey returned Bad Request (400) {}'.format(str(response.content)))
            raise EventsMonkeyAPIError('EventsMonkey returned {} error'.format(response.status_code))
