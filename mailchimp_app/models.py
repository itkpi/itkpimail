from customauth.models import User
from django.db import models
from events.fields import ExclusiveBooleanFieldOnOwnerGroups


class MailChimpCredential(models.Model):
    class Meta:
        unique_together = ('name', 'owner')
        verbose_name = "Mailchimp API Key"

    name = models.CharField(max_length=200, default='default')
    api_key = models.CharField(max_length=200)

    is_default = ExclusiveBooleanFieldOnOwnerGroups(default=True, verbose_name='Selected')
    owner = models.ForeignKey(User, null=True, editable=False)

    def __str__(self):
        return self.name
