from django.db import models

from redactor.fields import RedactorField
from exclusivebooleanfield.fields import ExclusiveBooleanField


class Event(models.Model):
    EASY = 'TRAINEE'
    MIDDLE = 'JUNIOR'
    HARDCORE = 'MIDDLE'

    LEVEL_OF_EVENT = (
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
                        default=""
                    )
    description = RedactorField(
                        verbose_name=u'Comment',
                        redactor_options={'lang': 'en', 'focus': 'true'},
                        allow_file_upload=False,
                        allow_image_upload=False
                    )
    speaker = models.CharField(max_length=200, default="")
    image_url = models.CharField(max_length=200, default="", blank=True)
    level = models.CharField(max_length=10, choices=LEVEL_OF_EVENT, default=EASY)
    place = models.CharField(max_length=200, null=True)
    when = models.DateTimeField(null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        if self.when:
            return '[%s] %s' % (self.when.strftime("%d/%m/%y"), self.title)
        else:
            return self.title

    def level_html(self):
        if self.level == Event.EASY:
            return '<span style="color: green">&#x25A0</span>'
        if self.level == Event.MIDDLE:
            return '<span style="color: yellow">&#x25B2</span>'
        if self.level == Event.HARDCORE:
            return '<span style="color: red">&#x25CF</span>'


class Template(models.Model):
    slug = models.CharField(max_length=80, default="unknown.html", unique=True)
    template_body = models.TextField(null=True)
    variables = models.CharField(max_length=200, help_text='"~!~"-separated variables list', default='', null=True, blank=True)
    is_default = ExclusiveBooleanField(default=False)

    def __str__(self):
        return self.slug


class Preview(models.Model):
    template = models.ForeignKey('Template')
    body = models.TextField(null=True)
    list_id = models.CharField(max_length=20, null=True)

    @models.permalink
    def get_absolute_url(self):
        return 'preview', [str(self.id)]
