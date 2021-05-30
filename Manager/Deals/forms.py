from django.utils.translation import ugettext_lazy as _
from sdh import forms
from django.shortcuts import get_object_or_404

from core.Deal.models import DealFile, Deal


class DealFileForm(forms.RequestForm):
    file = forms.FileField(label=_('File'), required=False)
    image = forms.ImageField(label=_('Image'), required=False)
    file_type = forms.ChoiceField(label=_('File type'))

    def __init__(self, *args, **kwargs):
        self.model = DealFile
        self.instance = kwargs.pop('instance', None)
        self.offer = kwargs.pop('offer', None)
        super(DealFileForm, self).__init__(*args, **kwargs)

        self.fields['file_type'].choices = DealFile.TYPES

        if self.instance:
            self.set_initial(self.instance)

    def clean(self):
        cleaned_data = self.cleaned_data

        if cleaned_data.get('file') and (cleaned_data.get('file_type') == DealFile.GALLERY or cleaned_data.get('file_type') == DealFile.COVER) or \
                cleaned_data.get('image') and cleaned_data.get('file_type') == DealFile.DOCUMENT or \
                cleaned_data.get('file') and cleaned_data.get('image'):
            raise forms.ValidationError(_('Enter correct file extension and not load both of them.'))

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
