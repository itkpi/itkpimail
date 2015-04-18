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


class Template(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
