from django.contrib.auth.models import User
from django.db import models
from events.fields import ExclusiveBooleanFieldOnOwnerGroups
import html2text
from redactor.fields import RedactorField


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


class VKGroup(models.Model):
    class Meta:
        verbose_name = "VK Group / Public"

    group_id = models.CharField(max_length=200)

    is_default = ExclusiveBooleanFieldOnOwnerGroups(default=True, verbose_name='Selected')
    owner = models.ForeignKey(User, null=True, editable=False)

    def __str__(self):
        return self.group_id


class Post(models.Model):
    content = RedactorField(
        redactor_options={'lang': 'en', 'focus': 'true'},
        allow_file_upload=False,
        allow_image_upload=False
    )

    vk_group = models.ForeignKey(VKGroup, null=True)
    owner = models.ForeignKey(User, null=False, editable=False)

    def __str__(self):
        return self.content

    def plain_content(self):
        return html2text.html2text(self.content)
