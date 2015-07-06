from django.template import loader, TemplateDoesNotExist
from events.models import *
from events.middlewares import get_current_request
from github import Github, UnknownObjectException
from itkpimail.settings import GITHUB_API_TOKEN


class MyLoader(loader.base.Loader):
    is_usable = True

    def load_template_source(self, template_name, template_dirs=None):
        request = get_current_request()
        try:
            git_remote = GitRemote.objects.get(owner__groups__in=request.user.groups.all())
            return self.load_template_source_from_git(git_remote.remote, template_name, template_dirs)
        except GitRemote.DoesNotExist:
            return self.load_template_source_from_database(request, template_name, template_dirs)


    def load_template_source_from_database(self, request, template_name, template_dirs=None):
        try:
            return Template.objects.get(slug=template_name, owner__groups__in=request.user.groups.all()).template_body, template_name
        except Template.DoesNotExist:
            raise TemplateDoesNotExist(template_name)

    def load_template_source_from_git(self, repo_user_and_name, template_name, template_dirs=None):
        github = Github(GITHUB_API_TOKEN)
        repo = github.get_repo(repo_user_and_name)
        try:
            return repo.get_file_contents(template_name).decoded_content.decode(), template_name
        except UnknownObjectException:
            raise TemplateDoesNotExist(template_name)
