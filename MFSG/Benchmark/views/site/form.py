from django import forms
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _

from ...models import Site


class Form(SuccessMessageMixin, forms.ModelForm):

    error_messages = {
        'path_incorrect': _("Strona o podanym adresie nie istnieje"),
        'no_measure': _("Musisz wybrać przynajmniej jedną miarę!")
    }

    path = forms.CharField(label="Adres strony")
    dom = forms.BooleanField(required=False)
    first_byte = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(Form, self).clean()

        dom = cleaned_data.get('dom')
        first_byte = cleaned_data.get('first_byte')
        if not dom and not first_byte:
            raise forms.ValidationError(
                self.error_messages['no_measure'],
                code='no_measure'
            )

        return cleaned_data

        #TODO sprawdzić, czy istnieje strona o takim adresie

    class Meta:
        model = Site
        fields = ["path", "dom", "first_byte"]