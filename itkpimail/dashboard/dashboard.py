"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'itkpimail.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'itkpimail.dashboard.CustomAppIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name
from itkpimail.dashboard.checker import ConfigurationChecker


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for itkpimail.
    """

    def init_with_context(self, context):
        if context.request.user.is_supreme:
            self.title = _("Welcome, Supreme User, The Greatest of all Users, My Creator!")
        else:
            self.title = _("Maillist Generation Engine")
        site_name = get_admin_site_name(context)

        links = []
        if context.request.tenant:
            company_name = context.request.tenant.group.name
            links.append({
                'title': _('Go to public events list of {}'.format(company_name)),
                'url': reverse('event_list'),
                'external': True,
                'description': _('Public page'),
                'attrs': {'target': '_blank'},
            })
            links.append({
                'title': _('Go to blog of {}'.format(company_name)),
                'url': reverse('blog_article_list'),
                'external': True,
                'description': _('Public page'),
                'attrs': {'target': '_blank'},
            })
        self.children.append(modules.LinkList(
            _('Quick links'),
            layout='stacked',  # inline
            draggable=False,
            deletable=False,
            collapsible=False,
            children=links,
        ))

        events_main = modules.ModelList(
            _('General'),
            models=('events.models.Event', 'events.models.SuggestedEvent', 'events.models.Preview', ),
        )
        events_admin = modules.ModelList(
            _('Configuration'),
            models=('events.*', 'mailchimp_app.*'),
            exclude=('events.models.Event', 'events.models.SuggestedEvent', 'events.models.Preview', ),
        )
        self.children.append(modules.Group(
            title=_('Digest Generator'),
            display="tabs",
            deletable=False,
            collapsible=False,
            children=[
                events_main,
                events_admin
            ]
        ))

        self.children.append(modules.ModelList(
            _('Blogs'),
            models=('blog.*',),
            deletable=False,
            collapsible=False,
        ))

        self.children.append(modules.ModelList(
            _('Administration'),
            deletable=False,
            collapsible=False,
            models=('customauth.*', 'hooks.*'),
        ))

        self.children.append(ConfigurationChecker())


class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for itkpimail.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
