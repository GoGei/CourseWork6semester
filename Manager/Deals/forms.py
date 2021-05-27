from django.utils.translation import ugettext_lazy as _
from sdh import forms
from django.shortcuts import get_object_or_404

from core.Deal.models import DealFile, DealGalleryFile, Deal


class DealFileForm(forms.RequestForm):
    file = forms.FileField(label=_('File'), required=True)

    def __init__(self, *args, **kwargs):
        self.model = DealFile
        self.instance = kwargs.pop('instance', None)
        self.offer = kwargs.pop('offer', None)
        super(DealFileForm, self).__init__(*args, **kwargs)

        if self.instance:
            self.set_initial(self.instance)

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data

    def save(self):
        instance = self.instance or self.model()
        self.set_model_fields(instance)
        deal = get_object_or_404(Deal, offer=self.offer)
        instance.deal = deal
        instance.save()
        return instance


class DealFileEditForm(DealFileForm):
    pass


class DealFileAddForm(DealFileForm):
    pass


class DealGalleryFileForm(forms.RequestForm):
    image = forms.ImageField(label=_('Image'), required=True)

    def __init__(self, *args, **kwargs):
        self.model = DealGalleryFile
        self.instance = kwargs.pop('instance', None)
        self.deal = kwargs.pop('deal', None)
        super(DealGalleryFileForm, self).__init__(*args, **kwargs)

        if self.instance:
            self.set_initial(self.instance)

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data

    def save(self):
        instance = self.instance or self.model()
        self.set_model_fields(instance)
        instance.deal = self.deal
        instance.save()
        return instance


class DealGalleryFileEditForm(DealFileForm):
    pass


class DealGalleryFileAddForm(DealFileForm):
    pass
