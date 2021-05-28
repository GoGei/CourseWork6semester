from django.conf import settings
from django.forms.formsets import BaseFormSet
from django.utils.translation import ugettext_lazy as _
from sdh import forms


class BaseLangForm(forms.RequestForm):
    language_code = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(BaseLangForm, self).__init__(*args, **kwargs)
        if self.initial.get('language_code') != settings.DEFAULT_LANGUAGE:
            for key, field in self.fields.items():
                if key != 'language_code':
                    field.required = False

    def save(self, obj):
        data = self.cleaned_data
        language_code = data['language_code']
        for field in obj.TRANSLATED_FIELDS:
            if field in self.fields:
                getattr(obj, '%s_data' % field)[language_code] = data[field]
        obj.save()


class BaseLangFormSet(BaseFormSet):

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', None)
        instance = kwargs.pop('instance', None)
        self.can_delete = True
        if 'can_delete' in kwargs:
            self.can_delete = kwargs.pop('can_delete')

        if not initial:
            allowed_languages = list(zip(*settings.LANGUAGES))[0]
            initial = [{'language_code': language} for language in allowed_languages]

        if instance:
            initial = instance.get_form_initial()

        super(BaseLangFormSet, self).__init__(*args, initial=initial, **kwargs)

    def clean(self):
        if any(self.errors):
            return
        if not any([not form.cleaned_data.get('delete') for form in self.forms]):
            raise forms.ValidationError(_("Set any value."))

    def get_forms(self):
        return [_form for _form in self.forms if _form.cleaned_data]

    def save(self, obj):
        for form in self.get_forms():
            data = form.cleaned_data
            if data['language_code']:
                form.save(obj)

