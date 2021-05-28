from core.Utils.base_classes import CrmMixin, TranslateMixin
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Offer(CrmMixin, TranslateMixin):
    TRANSLATED_FIELDS = ['header', 'text']
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
    header_data = JSONField(default=dict)  # {lang_code: data}
    text_data = JSONField(default=dict)  # {lang_code: data}
    state = models.CharField(max_length=16, choices=STATES)

    class Meta:
        db_table = 'offer'

    def __str__(self):
        return 'Offer: ' + self.address

    @property
    def label(self):
        return self.address

    @property
    def get_cover(self):
        from core.Deal.models import DealFile, Deal
        deal = Deal.objects.active().get(offer=self)
        files = DealFile.objects.active().filter(deal=deal)
        cover = files.filter(file_type=DealFile.COVER)
        if cover:
            return cover.first().image
        return None

    @property
    def get_gallery(self):
        from core.Deal.models import DealFile, Deal
        deal = Deal.objects.active().get(offer=self)
        files = DealFile.objects.active().filter(deal=deal)
        gallery = files.filter(file_type=DealFile.GALLERY)
        gallery = [item.image for item in gallery]
        return gallery
