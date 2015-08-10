from customauth.models import OwnedModel
from django.db import models
from django.utils.translation import ugettext_lazy as _


class BlogEntry(OwnedModel):
    class Meta:
        verbose_name = _('Blog post')
    title = models.CharField(max_length=256)
    slug = models.CharField(max_length=50, help_text=_('Unique string without special symbols.'
                                                       'Will be used in URL of blog post.'))
    content = models.TextField()
    tags = models.CharField(max_length=256)
    date_published = models.DateField()
    published = models.BooleanField(default=False, editable=False)
    personal = models.BooleanField(default=True, help_text=_('If checked, this post will not be shown in the'
                                                             'company blog, only on personal blog of author'))

    @models.permalink
    def get_absolute_url(self):
        return 'blog_post', [self.slug]
