from sdh import forms
from ckeditor.widgets import CKEditorWidget
from django.forms.formsets import formset_factory
from django.utils.translation import ugettext_lazy as _

from core.Offer.models import Offer
from django.contrib.auth.models import User
from core.Utils.lang_formset import BaseLangFormSet


class OfferForm(forms.RequestForm):
    address = forms.CharField(label=_('Address'), max_length=128)

    def __init__(self, *args, **kwargs):
        self.model = Offer
        self.instance = kwargs.pop('instance', None)
        super(OfferForm, self).__init__(*args, **kwargs)

        if self.instance:
            self.set_initial(self.instance)


class CreatedOfferForm(OfferForm):
    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data

    def save(self):
        instance = self.instance or self.model()
        self.set_model_fields(instance)
        instance.state = Offer.CREATED
        instance.save()

        return instance


class CreatedOfferEditForm(CreatedOfferForm):
    pass


class CreatedOfferAddForm(CreatedOfferForm):
    pass


class PickUpOfferForm(forms.RequestForm):
    address = forms.CharField(label=_('Address'), max_length=128)
    creator = forms.TypedChoiceField(label=_('Creator'),
                                     widget=forms.Select(attrs={'class': 'form-control select2',
                                                                'data-placeholder': _('Select from the list')}),
                                     coerce=lambda pk: User.objects.all().get(pk=pk))
    manager = forms.TypedChoiceField(label=_('Manager'),
                                     widget=forms.Select(attrs={'class': 'form-control select2',
                                                                'data-placeholder': _('Select from the list')}),
                                     coerce=lambda pk: User.objects.filter(is_staff=True).get(pk=pk))
    clients = forms.TypedMultipleChoiceField(label=_('Clients'),
                                             widget=forms.SelectMultiple(
                                                 attrs={'class': 'select2 select2-multiple', 'data-placeholder': _(
                                                     'Select from the list')}),
                                             coerce=lambda pk: User.objects.filter(is_staff=False).get(pk=pk)
                                             )

    def __init__(self, *args, **kwargs):
        self.model = Offer
        self.instance = kwargs.pop('instance', None)
        super(PickUpOfferForm, self).__init__(*args, **kwargs)

        creator_qs = User.objects.all().order_by('-id')
        self.populate('creator', creator_qs)

        manager_qs = User.objects.filter(is_staff=True).all().order_by('-id')
        self.populate('manager', manager_qs)

        clients_qs = User.objects.filter(is_staff=False).all().order_by('-id')
        self.populate('clients', clients_qs)

        if self.instance:
            self.set_initial(self.instance)

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data

    def save(self):
        instance = self.instance or self.model()
        self.set_model_fields(instance)
        instance.state = Offer.PICK_UP
        instance.save()

        return instance


class PickUpOfferEditForm(PickUpOfferForm):
    pass


class OfferLangForm(forms.RequestForm):
    language_code = forms.CharField(label=_('Language'), widget=forms.HiddenInput)

    header = forms.CharField(label=_('Header'), max_length=30)
    text = forms.CharField(label=_('Text'), max_length=500, widget=CKEditorWidget(config_name='user'))

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.model = Offer

    def clean(self):
        if any(self.errors):
            return
        data = self.cleaned_data
        return data

    def save(self, obj):
        data = self.cleaned_data
        language_code = data['language_code']
        obj.header_data[language_code] = data['header']
        obj.text_data[language_code] = data['text']
        obj.save()
        return None


class OfferFormSet(BaseLangFormSet):
    def save(self, obj):
        for form in self.get_forms():
            data = form.cleaned_data
            if data['language_code'] and data['header'] and data['text']:
                form.save(obj)

    def clean(self):
        def save(self, obj):
            for form in self.get_forms():
                form.save(obj)


OfferLangFormSet = formset_factory(OfferLangForm, formset=OfferFormSet, extra=0)
