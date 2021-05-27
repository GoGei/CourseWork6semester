from core.Utils.base_classes import CrmMixin, TranslateMixin
from django.contrib.auth.models import User
from core.Offer.models import Offer
from django.db import models
from django.utils.translation import ugettext_lazy as _


class OfferRequest(CrmMixin, TranslateMixin):
    VIEWED_BY_USER = 'viewed_by_user'
    VIEWED_BY_MANAGER = 'viewed_by_manager'
    DECLINED = 'declined'
    ACCEPTED = 'accepted'

    STATES = (
        (VIEWED_BY_USER, _('Viewed by user')),
        (VIEWED_BY_MANAGER, _('Viewed by manager')),
        (DECLINED, _('Declined')),
        (ACCEPTED, _('Accepted')),
    )

    offer = models.ForeignKey(Offer, on_delete=models.PROTECT, related_name='+')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')

    state = models.CharField(max_length=16, choices=STATES)

    class Meta:
        db_table = 'offer_request'

    def __str__(self):
        return 'OfferRequest: ' + self.address

    @property
    def label(self):
        return self.address
