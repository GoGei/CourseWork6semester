from django.utils.translation import ugettext_lazy as _
from core.Utils.fields import PhoneField
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    last_name = forms.CharField(label=_('Last name'), max_length=50, required=True,
                                widget=forms.TextInput(attrs={'placeholder': _('Enter last name')}))
    first_name = forms.CharField(label=_('First name'), max_length=50, required=True,
                                 widget=forms.TextInput(attrs={'placeholder': _('Enter first name')}))
    phone = PhoneField(label=_('Phone'), attrs={'placeholder': _('Enter phone')})
    email = forms.EmailField(label=_('Email'), max_length=50, required=True,
                             widget=forms.TextInput(attrs={'placeholder': _('Enter email')}))

    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'phone', 'email', 'password1', 'password2']
