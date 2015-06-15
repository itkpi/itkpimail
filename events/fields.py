# https://github.com/anentropic/django-exclusivebooleanfield/blob/master/exclusivebooleanfield/fields.py


from django.db import models, transaction
from django.db.models import Q

from six import string_types
from six.moves import reduce


try:
    transaction_context = transaction.atomic
except AttributeError:
    transaction_context = transaction.commit_on_success


class ExclusiveBooleanFieldOnOwnerGroups(models.BooleanField):
    def __init__(self, on=None, *args, **kwargs):
        if isinstance(on, string_types):
            on = (on, )
        self._on_fields = on or ()
        super().__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        super().contribute_to_class(cls, name)
        models.signals.class_prepared.connect(self._replace_save, sender=cls)

    def _replace_save(self, sender, **kwargs):
        old_save = sender.save
        field_name = self.name
        on_fields = self._on_fields

        def new_save(self, *args, **kwargs):
            with transaction_context():
                if getattr(self, field_name) is True:
                    u_args = {field_name: False}
                    sender._default_manager.filter(owner__groups__in=self.owner.groups.all()).update(**u_args)
                old_save(self, *args, **kwargs)
        new_save.alters_data = True

        sender.save = new_save
