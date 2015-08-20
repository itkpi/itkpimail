from http.server import SimpleHTTPRequestHandler, BaseHTTPRequestHandler, HTTPServer
import logging
from threading import Thread
from customauth.tests import TenantTestMixin
from django.test import TestCase
from hooks.models import Hook
from hooks.views import call_hook

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)

TEST_EVENT = 'TEST_EVENT'


class RecordRequestsServer(HTTPServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.recorded = []

    def add_record(self, method, path, content):
        self.recorded.append((method, path, content))


class SayOKHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b'OK')
        self.server.add_record(self.command, self.path, None)

    def do_POST(self):
        content = self.rfile.read(int(self.headers['content-length']))
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b'OK')
        self.server.add_record(self.command, self.path, content)


class OutgoingHookTest(TenantTestMixin, TestCase):
    def shutdown_server(self, httpd, httpd_thread):
        httpd.shutdown()
        httpd_thread.join()

    def start_server(self):
        httpd = RecordRequestsServer(("127.0.0.1", 0), SayOKHandler)
        addr = httpd.socket.getsockname()
        httpd_thread = Thread(target=httpd.serve_forever)
        httpd_thread.start()
        return addr, httpd, httpd_thread

    def test_simple(self):
        addr, httpd, httpd_thread = self.start_server()

        hook = Hook(event=TEST_EVENT, url='http://{}:{}/addr'.format(addr[0], addr[1]),
                    method='POST', body='content', group=self.group)
        hook.save()

        call_hook(TEST_EVENT, None)

        self.shutdown_server(httpd, httpd_thread)
        self.assertEqual(httpd.recorded, [('POST', '/addr', b'content')])

    def test_template(self):
        addr, httpd, httpd_thread = self.start_server()

        hook = Hook(event=TEST_EVENT, url='http://{}:{}/addr'.format(addr[0], addr[1]),
                    method='POST', body='content {{ object.data }}', group=self.group)
        hook.save()

        call_hook(TEST_EVENT, {'data': '123'})

        self.shutdown_server(httpd, httpd_thread)
        self.assertEqual(httpd.recorded, [('POST', '/addr', b'content 123')])

    def test_no_hook(self):
        addr, httpd, httpd_thread = self.start_server()

        call_hook(TEST_EVENT, None)

        self.shutdown_server(httpd, httpd_thread)
        self.assertEqual(httpd.recorded, [])
