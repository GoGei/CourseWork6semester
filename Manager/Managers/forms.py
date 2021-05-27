from django.utils.translation import ugettext_lazy as _
from sdh import forms

from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class ManagerForm(forms.RequestForm):
    password_validator_regex = RegexValidator(regex=r'^[\dA-Za-z!@-]{8,}$',
                                              message=_(
                                                  'Enter minimum eight characters, using numbers, letters, symbols (1-0, A-Z, a-z, !@-).'))

    first_name = forms.CharField(label=_('First name'), max_length=30)
    last_name = forms.CharField(label=_('Last name'), max_length=30)
    email = forms.EmailField(label=_('Email'), max_length=128)
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput,
                               validators=[password_validator_regex])
    repeat_password = forms.CharField(label=_('Repeat password'),
                                      widget=forms.PasswordInput,
                                      validators=[password_validator_regex])

    def __init__(self, *args, **kwargs):
        self.model = User
        self.instance = kwargs.pop('instance', None)
        super(ManagerForm, self).__init__(*args, **kwargs)

        if self.instance:
            self.set_initial(self.instance)

    def clean_email(self):
        cleaned_data = super(ManagerForm, self).clean()

        email = cleaned_data['email']
        qs = self.model.objects.filter(email__iexact=email)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.count():
            raise forms.ValidationError(_('User with this email already exists'))

        return email.lower()

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        repeated_password = cleaned_data.get('repeat_password')
        if password and repeated_password and password != repeated_password:
            self.add_error('password', _('Password mismatch!'))
            self.add_error('repeated_password', _('Password mismatch!'))

        return cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get('email')
        user = User.objects.filter(email=email)
        if not user:
            user = User.objects.create_superuser(username=cleaned_data.get('email'),
                                                 email=cleaned_data.get('email'),
                                                 password=cleaned_data.get('password'))
        else:
            user = User.objects.get(email=email)

        user.first_name = cleaned_data.get('first_name')
        user.last_name = cleaned_data.get('last_name')
        user.email = cleaned_data.get('email')
        user.is_superuser = False
        user.is_staff = True
        user.set_password(cleaned_data.get('password'))
        user.save()

        return user


class ManagerEditForm(ManagerForm):
    pass


class ManagerAddForm(ManagerForm):
    pass
