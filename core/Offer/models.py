from core.Utils.base_classes import CrmMixin, TranslateMixin
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Offer(CrmMixin, TranslateMixin):
    CREATED = 'created'
    PICK_UP = 'pick_up'
    CLOSED = 'closed'
    DENY = 'deny'

    STATES = (
        (CREATED, _('Created')),
        (PICK_UP, _('Pick up')),
        (CLOSED, _('Closed')),
        (DENY, _('Deny')),
    )

    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+', null=True)
    manager = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+', null=True)
    clients = models.ManyToManyField(User, related_name='+')

    address = models.CharField(max_length=128)
    state = models.CharField(max_length=16, choices=STATES)

    class Meta:
        db_table = 'offer'

    def __str__(self):
        return 'Offer: ' + self.address

    @property
    def label(self):
        return self.address
