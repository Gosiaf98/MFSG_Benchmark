from django import forms
from ...models import Site


class Form(forms.ModelForm):

    path = forms.CharField(label="Adres strony")
    dom = forms.BooleanField(required=False)
    first_byte = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)

    class Meta:
        model = Site
        fields = ["path", "dom", "first_byte"]

    def full_clean(self):
        cleaned_data = super(Form, self).clean()

        dom = self.cleaned_data.get('dom')
        first_byte = self.cleaned_data.get('first_byte')

        print("???")

        return self.cleaned_data

        #TODO sprawdzić, czy istnieje strona o takim adresie