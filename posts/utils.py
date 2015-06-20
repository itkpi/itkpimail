import http.cookiejar
import urllib.request
import json

from posts.models import VKApp, VKCredential
import vk


def get_vk_api(request):
    vk_app = VKApp.objects.get(is_default=True, owner__groups__in=request.user.groups.all())
    vk_credential = VKCredential.objects.get(owner=request.user)

    vkapi = vk.API(vk_app.app_id, access_token=vk_credential.access_token, scope='wall')
    return vkapi


def server_oauth_by_code(code, app_id, secret):
    access_token_url = ('https://oauth.vk.com/access_token?'
                        'client_id={}&'
                        'client_secret={}&'
                        'code={}&'
                        'redirect_uri=https://oauth.vk.com/blank.html&'
                        'grant_type=client_credentials'). \
        format(app_id, secret, code)
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()),
        urllib.request.HTTPRedirectHandler()
    )
    response = opener.open(access_token_url)
    access_token_json = json.loads(response.read().decode())
    return access_token_json['access_token']
