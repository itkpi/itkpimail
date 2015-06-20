from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from posts.forms import VKAuthForm
from posts.models import VKApp, VKCredential, Post
from posts.utils import get_vk_api, server_oauth_by_code


class VKAuthView(FormView):
    form_class = VKAuthForm
    template_name = 'vk/auth.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        url = form.cleaned_data['url']
        access_token = self.get_access_token_from_url(url)

        vk_app = VKApp.objects.get(is_default=True, owner__groups__in=self.user.groups.all())
        VKCredential.objects.filter(owner=self.user, app=vk_app).delete()  # remove previous credentials

        credential = VKCredential()
        credential.owner = self.user
        credential.access_token = access_token
        credential.app = vk_app
        credential.save()
        return redirect(reverse("admin:posts_vkcredential_changelist"))

    def get_var_from_url(self, url, variable):
        data = url.split("#")[1]
        code = None
        for param in data.split("&"):
            key, value = param.split("=")
            if key == variable:
                code = value
                break
        return code

    def get_access_token_from_url(self, url):
        token = self.get_var_from_url(url, 'access_token')
        if token:
            return token

        code = self.get_var_from_url(url, 'code')
        vk_app = VKApp.objects.get(is_default=True, owner__groups__in=self.user.groups.all())
        return server_oauth_by_code(code, vk_app.app_id, vk_app.secret)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vk_app = VKApp.objects.get(is_default=True, owner__groups__in=self.user.groups.all())
        # redirect_url = request.build_absolute_uri(reverse("admin:posts_vkcredential_auth_done"))
        vk_oauth_url = ('https://oauth.vk.com/authorize?client_id={}&'
                        'scope=wall&'
                        'redirect_uri=https://oauth.vk.com/blank.html&'
                        'display=page&v=5.34&'
                        'response_type=token').format(vk_app.app_id)
        context['vk_oauth_url'] = vk_oauth_url
        return context


@staff_member_required
def publish_to_vk(request, model_id):
    post = Post.objects.get(pk=model_id)
    vk_api = get_vk_api(request)
    group_id = vk_api.groups.getById(group_id=post.vk_group.group_id)[0]['id']
    vk_api.wall.post(message=post.plain_content(), owner_id=-group_id, from_group=1)
    response = render_to_response("vk/published.html")
    response['Refresh'] = '3;url={}'.format(reverse('admin:posts_post_change', args=[model_id]))
    return response
