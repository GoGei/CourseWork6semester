import re

from django import forms
from django.core.exceptions import ValidationError
from django.utils.encoding import smart_text
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


def cell_phone_validator_ukraine(value):
    regex = r"\+38(\d{3})\d{7}"

    rc = re.findall(regex, value)

    if not rc:
        raise ValidationError(_('Phone has incorrect format. Please use +380 (99) 999-9999'))


class NullBooleanField(forms.NullBooleanField):
    def __init__(self, *args, **kwargs):
        super(NullBooleanField, self).__init__(*args, **kwargs)
        self.widget.choices[0] = ('0', '------')


class PhoneField(forms.CharField):
    def __init__(self, *args, **kwargs):
        self.max_length = 20

        attrs = {"data-inputmask": mark_safe("'mask': '+380 (99) 999-9999'"),
                                             "data-masked": ""}
        attrs.update(kwargs.pop('attrs', {}))

        self.widget = forms.TextInput(attrs=attrs)
        super(PhoneField, self).__init__(*args, **kwargs)
        self.validators.append(cell_phone_validator_ukraine)

    def to_python(self, value):
        "Returns a Unicode object."
        if value in self.empty_values:
            return ''
        value = re.sub(r'[\s|\(|\)|-]', r'', value)
        return smart_text(value)
