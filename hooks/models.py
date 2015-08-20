from customauth.models import GroupOwnedModel
from django.db import models

POST_PUBLISHED_PERSONAL = 'blog_post_published_personal'
POST_PUBLISHED = 'blog_post_published'
EVENT_SUGGESTED = 'event_suggested'


class Hook(GroupOwnedModel):
    event = models.CharField(max_length=50, choices=((EVENT_SUGGESTED, 'Event suggested'),
                                                     (POST_PUBLISHED, 'Blog post published'),
                                                     (POST_PUBLISHED_PERSONAL, 'Personal blog post published')))
    url = models.URLField()
    method = models.CharField(max_length=10, choices=(('GET', 'GET'), ('POST', 'POST')))
    body = models.TextField(help_text="Template for POST request. You can use variable 'object'.")


IN_EVENT_SUGGEST = 'event_suggest'


class IncomingHook(GroupOwnedModel):
    event = models.CharField(max_length=50, choices=((IN_EVENT_SUGGEST, 'Suggest event'),
                                                     ))
    name = models.CharField(max_length=50, help_text='Who will use it')
    key = models.CharField(max_length=50)
