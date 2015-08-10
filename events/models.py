from django.utils.translation import ugettext_lazy as _
from customauth.models import OwnedModel, GroupOwnedModel
from django.db import models
from django.db.models import Q

from redactor.fields import RedactorField
from events.fields import ExclusiveBooleanFieldOnOwnerGroups


def filter_by_owner_group(queryset, request):
    queryset = queryset.filter(owner__isnull=False)
    q = Q()
    for group in request.user.groups.all():
        q |= Q(owner__groups=group)
    return queryset.filter(q).distinct()


class BaseEvent(models.Model):
    class Meta:
        abstract = True
    EMPTY = 'NONE'
    EASY = 'TRAINEE'
    MIDDLE = 'JUNIOR'
    HARDCORE = 'MIDDLE'

    LEVEL_OF_EVENT = (
        (EMPTY, 'none'),
        (EASY, 'trainee'),
        (MIDDLE, 'junior'),
        (HARDCORE, 'middle'),
    )

    title = models.CharField(max_length=200)
    agenda = RedactorField(
                        verbose_name=_('Agenda'),
                        redactor_options={'lang': 'en', 'focus': 'true'},
                        allow_file_upload=False,
                        allow_image_upload=False,
                        default=_("""
                                <strong>Програма:</strong><br/>
                                <ul>
                                <li></li>
                                </ul>
                                <strong>Спікери:</strong><br/>
                                <ul>
                                <li>&nbsp;</li>
                                </ul>
                                """)
                    )
    social = RedactorField(
                        verbose_name=u'Social',
                        help_text=_('How to get to the event, useful links and comments'),
                        redactor_options={'lang': 'en', 'focus': 'true'},
                        allow_file_upload=False,
                        allow_image_upload=False
                    )
    image_url = models.CharField(max_length=200, default="")
    level = models.CharField(max_length=10, choices=LEVEL_OF_EVENT, default=EMPTY)
    place = models.CharField(max_length=200, null=True)
    when = models.DateField(null=True, help_text='Event beginning date')
    when_time = models.TimeField(null=True, blank=True, help_text='Event beginning time')
    when_end = models.DateField(null=True, blank=True, help_text='Event ending date')
    when_end_time = models.TimeField(null=True, blank=True, help_text='Event ending time')
    when_time_required = models.BooleanField(default=True)
    publish = models.BooleanField(default=False, help_text=_(u'This event will be published on your company\'s page'))
    registration = models.CharField(max_length=200, default="")

    special = models.BooleanField(default=False, help_text=_('This event will be published in special way (if template '
                                                             'supports it). You can set special on "promoted" events or '
                                                             'some events you wish to draw attention to.'))

    def __str__(self):
        if self.when:
            return '[%s] %s' % (self.when.strftime("%d/%m/%y"), self.title)
        else:
            return self.title


class Template(OwnedModel):
    class Meta:
        unique_together = ['slug', 'owner']
        verbose_name = _("Email Template (Deprecated. Use Github Remote)")
        verbose_name_plural = _("Email Templates (Deprecated. Use Github Remote)")
    slug = models.CharField(max_length=80, default="unknown.html")
    template_body = models.TextField(null=True)
    variables = models.CharField(max_length=200, help_text=_('"~!~"-separated variables list'), default='', null=True, blank=True)
    is_default = ExclusiveBooleanFieldOnOwnerGroups(default=False)

    def __str__(self):
        return self.slug


class GitRemote(OwnedModel):
    class Meta:
        unique_together = ('remote', 'owner')
        verbose_name = _("Github remote with Email Templates")
        verbose_name_plural = _("Github remotes with Email Templates")
    remote = models.CharField(max_length=200)

    is_default = ExclusiveBooleanFieldOnOwnerGroups(default=True, verbose_name='Selected',
                                                    help_text=_('If any of remotes is selected, it will be used. '
                                                                'Otherwise, Templates from DB will be used.'))

    def __str__(self):
        return self.remote


class Preview(OwnedModel):
    published = models.BooleanField(default=False)
    body = models.TextField(null=True)
    list_id = models.CharField(max_length=20, null=True)
    mailchimp_url = models.CharField(max_length=200, null=True, blank=True, editable=False)

    @models.permalink
    def get_absolute_url(self):
        return 'preview', [str(self.id)]


class Event(BaseEvent, OwnedModel):
    previews = models.ManyToManyField('Preview')
    date = models.DateTimeField(auto_now_add=True, blank=True, verbose_name=_(u"Created datetime"))


class SuggestedEvent(BaseEvent, GroupOwnedModel):
    suggested_by = models.CharField(max_length=200, editable=False, default='anonymous')
    date = models.DateTimeField(auto_now_add=True, blank=True, verbose_name=_("Submitted"))
