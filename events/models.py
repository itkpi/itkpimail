from django.db import models


class Event(models.Model):
    EASY = 'NOOB'
    MIDDLE = 'PADAWAN'
    HARDCORE = 'JEDI'

    LEVEL_OF_EVENT = (
        (EASY, 'noob'),
        (MIDDLE, 'padawan'),
        (HARDCORE, 'jedi'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    level = models.CharField(max_length=10, choices=LEVEL_OF_EVENT, default=EASY)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return "[%s] %s" % (self.date.strftime("%d/%m/%y"), self.title)


class Template(models.Model):
    slug = models.CharField(max_length=80, default="unknown.html", unique=True)
    template_body = models.TextField(null=True)
    variables = models.CharField(max_length=200, help_text='"~!~"-separated variables list', default='')

    def __str__(self):
        return self.slug


class Preview(models.Model):
    template = models.ForeignKey('Template')
    body = models.TextField(null=True)
    list_id = models.CharField(max_length=20, null=True)

    @models.permalink
    def get_absolute_url(self):
        return 'preview', [str(self.id)]
