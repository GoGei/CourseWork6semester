from django import forms


class NullBooleanField(forms.NullBooleanField):
    def __init__(self, *args, **kwargs):
        super(NullBooleanField, self).__init__(*args, **kwargs)
        self.widget.choices[0] = ('0', '------')
