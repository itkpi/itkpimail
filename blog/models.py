from customauth.models import OwnedModel
from django.db import models


class BlogEntry(OwnedModel):
    title = models.CharField(max_length=256)
    slug = models.CharField(max_length=50)
    content = models.TextField()
    tags = models.TextField()
