from __future__ import unicode_literals

import sdh.forms as forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth.models import User


class AuthenticationForm(forms.RequestForm):
    email = forms.EmailField(label=_('Login'), required=True)
    password = forms.CharField(label=_('Password'), required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': _('Password'),
                                                                 'type': 'password'}),
                               validators=[validate_password])

    def clean_email(self):
        cleaned_data = super(AuthenticationForm, self).clean()
        email = cleaned_data['email'].lower()
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError(_('Unknown login.'))
        return email
