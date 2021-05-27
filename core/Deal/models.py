import os

from django.db import models
from django.contrib.auth.models import User

from core.Utils.base_classes import CrmMixin, TranslateMixin


class Deal(CrmMixin, TranslateMixin):
    manager = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')
    client = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')
    offer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')

    class Meta:
        db_table = 'deal'

    def __str__(self):
        return self.address

    @property
    def label(self):
        return self.address


class DealFile(CrmMixin, TranslateMixin):
    deal = models.ForeignKey('Deal.Deal', on_delete=models.PROTECT)
    file = models.ImageField()
    content_type = models.CharField(max_length=100)

    class Meta:
        db_table = 'deal_file'

    def __str__(self):
        return 'Deal file: ' + str(self.pk)

    @property
    def filename(self):
        return os.path.basename(self.file.name)
