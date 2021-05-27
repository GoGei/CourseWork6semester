from core.Utils.base_classes import CrmMixin, TranslateMixin
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Offer(CrmMixin, TranslateMixin):
    CREATED = 'created'
    NEW = 'new'
    GOT = 'got'
    CLOSED = 'closed'

    STATES = (
        (CREATED, _('Created')),
        (NEW, _('New')),
        (GOT, _('Got')),
        (CLOSED, _('Closed')),
    )

    creator = models.ForeignKey(User, on_delete=models.PROTECT)

    manager = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')
    client = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')

    address = models.CharField(max_length=128)
    state = models.CharField(max_length=16, choices=STATES)

    class Meta:
        db_table = 'offer'

    def __str__(self):
        return self.address

    @property
    def label(self):
        return self.address
