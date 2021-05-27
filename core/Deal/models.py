import os

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from core.Offer.models import Offer

from core.Utils.base_classes import CrmMixin, TranslateMixin


class Deal(CrmMixin, TranslateMixin):
    manager = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')
    offer = models.ForeignKey(Offer, on_delete=models.PROTECT, related_name='+')

    class Meta:
        db_table = 'deal'

    def __str__(self):
        return 'Deal: ' + str(self.pk)

    @property
    def label(self):
        return self.address


class DealFile(CrmMixin, TranslateMixin):
    COVER = 'cover'
    GALLERY = 'gallery'
    DOCUMENT = 'document'

    TYPES = (
        (COVER, _('Cover')),
        (GALLERY, _('Gallery')),
        (DOCUMENT, _('Document')),
    )

    deal = models.ForeignKey('Deal.Deal', on_delete=models.PROTECT)
    file = models.FileField(null=True)
    image = models.ImageField(null=True)
    file_type = models.CharField(max_length=16, choices=TYPES, null=True)

    class Meta:
        db_table = 'deal_file'

    def __str__(self):
        return 'Deal file: ' + str(self.pk)

    @property
    def filename(self):
        return os.path.basename(self.file.name)
