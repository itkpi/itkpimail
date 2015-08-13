import logging
from django.template import loader, TemplateDoesNotExist
from events.models import *
from events.middlewares import get_current_request
from github import Github, UnknownObjectException
from itkpimail.settings import GITHUB_API_TOKEN


logger = logging.getLogger(__name__)


def is_github_remote_enabled(request):
    return GitRemote.objects.filter(owner__groups__in=request.user.groups.all()).exists()


def get_github_repo(request):
    git_remote = GitRemote.objects.get(owner__groups__in=request.user.groups.all())

    github = Github(GITHUB_API_TOKEN)
    repo_user_and_name = git_remote.remote
    return github.get_repo(repo_user_and_name)


class MyLoader(loader.base.Loader):
    is_usable = True

    def load_template_source(self, template_name, template_dirs=None):
        request = get_current_request()
        if not request:
            raise TemplateDoesNotExist(template_name)
        if template_name.startswith("admin/"):
            raise TemplateDoesNotExist(template_name)

        if is_github_remote_enabled(request):
            return self.load_template_source_from_git(request, template_name, template_dirs)
        else:
            return self.load_template_source_from_database(request, template_name, template_dirs)

    def load_template_source_from_database(self, request, template_name, template_dirs=None):
        try:
            return Template.objects.get(slug=template_name, owner__groups__in=request.user.groups.all()).template_body, template_name
        except Template.DoesNotExist:
            raise TemplateDoesNotExist(template_name)

    def load_template_source_from_git(self, request, template_name, template_dirs=None):
        try:
            logger.info("Loading template {} from GitHub".format(template_name))
            repo = get_github_repo(request)
            return repo.get_file_contents(template_name).decoded_content.decode(), template_name
        except UnknownObjectException:
            raise TemplateDoesNotExist(template_name)
