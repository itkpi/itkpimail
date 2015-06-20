from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from posts.models import VKApp, VKCredential


@staff_member_required
def vk_auth_view(request):
    vk_app = VKApp.objects.get(is_default=True, owner__groups__in=request.user.groups.all())
    redirect_url = request.build_absolute_uri(reverse("admin:posts_vkcredential_auth_done"))
    vk_auth_url = ("https://oauth.vk.com/authorize?client_id={}&"
                   "scope=wall&"
                   "redirect_uri={}&"
                   "display=page&v=5.34&"
                   "response_type=token").format(vk_app.app_id, redirect_url)
    return redirect(vk_auth_url)


@staff_member_required
def vk_auth_done_view(request):
    return render_to_response('vk/auth_done.html')

@staff_member_required
def vk_auth_save_view(request, access_token):
    vk_app = VKApp.objects.get(is_default=True, owner__groups__in=request.user.groups.all())

    VKCredential.objects.filter(owner=request.user, app=vk_app).delete()  # remove previous credentials

    credential = VKCredential()
    credential.owner = request.user
    credential.access_token = access_token
    credential.app = vk_app
    credential.save()
    return redirect(reverse("admin:posts_vkcredential_changelist"))