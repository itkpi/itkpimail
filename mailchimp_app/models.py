from django.utils.translation import ugettext_lazy as _
from customauth.models import User, OwnedModel
from django.db import models
from events.fields import ExclusiveBooleanFieldOnOwnerGroups


class MailChimpCredential(OwnedModel):
    class Meta:
        unique_together = ('name', 'owner')
        verbose_name = _("Mailchimp API Key")

    name = models.CharField(max_length=200, default='default')
    api_key = models.CharField(max_length=200)

    is_default = ExclusiveBooleanFieldOnOwnerGroups(default=True, verbose_name=_('Selected'))

    def __str__(self):
        return self.name
