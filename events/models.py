from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

from redactor.fields import RedactorField
#from exclusivebooleanfield.fields import ExclusiveBooleanField
from events.fields import ExclusiveBooleanFieldOnOwnerGroups


def filter_by_owner_group(queryset, request):
    queryset = queryset.filter(owner__isnull=False)
    q = Q()
    for group in request.user.groups.all():
        q |= Q(owner__groups=group)
    return queryset.filter(q).distinct()


class Event(models.Model):
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
                        verbose_name=u'Agenda',
                        redactor_options={'lang': 'en', 'focus': 'true'},
                        allow_file_upload=False,
                        allow_image_upload=False,
                        default="""
                                <strong>Програма:</strong><br/>
                                <ul>
                                <li></li>
                                </ul>
                                <strong>Спікери:</strong><br/>
                                <ul>
                                <li>&nbsp;</li>
                                </ul>
                                """
                    )
    social = RedactorField(
                        verbose_name=u'Social',
                        redactor_options={'lang': 'en', 'focus': 'true'},
                        allow_file_upload=False,
                        allow_image_upload=False
                    )
    image_url = models.CharField(max_length=200, default="")
    level = models.CharField(max_length=10, choices=LEVEL_OF_EVENT, default=EMPTY)
    place = models.CharField(max_length=200, null=True)
    when = models.DateField(null=True)
    when_time = models.TimeField(null=True, blank=True)
    when_end = models.DateField(null=True, blank=True)
    when_end_time = models.TimeField(null=True, blank=True)
    when_time_required = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, verbose_name=u"Created datetime")
    registration = models.CharField(max_length=200, default="")

    special = models.BooleanField(default=False, help_text=u'This event will be published in special way (if template '
                                                           'supports it). You can set special on "promoted" events or '
                                                           'some events you wish to draw attention to.')

    owner = models.ForeignKey(User, null=True, editable=False, verbose_name=u"Created by")
    previews = models.ManyToManyField('Preview')

    def __str__(self):
        if self.when:
            return '[%s] %s' % (self.when.strftime("%d/%m/%y"), self.title)
        else:
            return self.title


class Template(models.Model):
    class Meta:
        unique_together = ['slug', 'owner']
    slug = models.CharField(max_length=80, default="unknown.html")
    template_body = models.TextField(null=True)
    variables = models.CharField(max_length=200, help_text='"~!~"-separated variables list', default='', null=True, blank=True)
    is_default = ExclusiveBooleanFieldOnOwnerGroups(default=False)

    owner = models.ForeignKey(User, null=True, editable=False)

    def __str__(self):
        return self.slug


class Preview(models.Model):
    published = models.BooleanField(default=False)
    body = models.TextField(null=True)
    list_id = models.CharField(max_length=20, null=True)
    mailchimp_url = models.CharField(max_length=200, null=True, blank=True, editable=False)

    owner = models.ForeignKey(User, null=True, editable=False)

    @models.permalink
    def get_absolute_url(self):
        return 'preview', [str(self.id)]
