from django.contrib.auth.models import User
from django.db import models
from events.fields import ExclusiveBooleanFieldOnOwnerGroups


class VKApp(models.Model):
    class Meta:
        unique_together = ('name', 'owner')
        verbose_name = "VK Application"

    name = models.CharField(max_length=200, default='default')
    app_id = models.IntegerField()
    secret = models.CharField(max_length=200)

    is_default = ExclusiveBooleanFieldOnOwnerGroups(default=True, verbose_name='Selected')
    owner = models.ForeignKey(User, null=True, editable=False)

    def __str__(self):
        return self.name


class VKCredential(models.Model):
    class Meta:
        unique_together = ('owner', 'app')
        verbose_name = "VK Credential"

    access_token = models.CharField(max_length=200)
    app = models.ForeignKey(VKApp, null=False)
    owner = models.ForeignKey(User, null=True, editable=False)

    def __str__(self):
        return self.app.name
