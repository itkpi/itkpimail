from admin_tools.dashboard import modules
from events.loaders import is_github_remote_enabled
from events.mailchimp_utils import is_mailchimp_configured
from itkpimail import settings


class ConfigurationChecker(modules.DashboardModule):
    deletable = False
    collapsible = False

    def is_empty(self):
        return False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Configuration check"
        self.template = 'my_blocks/checker.html'
        self.github_configured = False
        self.mailchimp_configured = False

    def init_with_context(self, context):
        super().init_with_context(context)
        request = context['request']
        self.github_configured = is_github_remote_enabled(request)
        self.github_configured_auth = (settings.GITHUB_API_TOKEN is not None)\
                                      and (settings.GITHUB_API_TOKEN.strip() != '')
        self.mailchimp_configured = is_mailchimp_configured(request)
