from django.utils.translation import ugettext_lazy as _
from sdh import forms

from core.Offer.models import Offer
from django.contrib.auth.models import User


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
                                                 attrs={'class': 'select2', 'data-placeholder': _(
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
