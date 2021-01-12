from django import forms
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


from ...models import Site


class Form(SuccessMessageMixin, forms.ModelForm):

    driver = webdriver.Chrome(ChromeDriverManager().install())

    error_messages = {
        'path_incorrect': _("Strona o podanym adresie nie istnieje"),
        'no_measure': _("Musisz wybrać przynajmniej jedną miarę!")
    }

    path = forms.CharField(label="<b>Adres strony</b>")
    dom = forms.BooleanField(required=False)
    first_byte = forms.BooleanField(required=False)

    SITES_TO_COMPARE = (
        ("1", "One"),
        ("2", "Two"),
        ("3", "Three"),
        ("4", "Four"),
        ("5", "Five"),
    )
    compare_sites = forms.MultipleChoiceField(widget=forms.SelectMultiple, choices=SITES_TO_COMPARE, label="<b>Wybierz strony, z którymi chcesz się porównać:</b>", required=False)

    def __init__(self, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)

    def time_url(self, driver, url):
        driver.get(url)

        navigation_start = driver.execute_script(
            "return window.performance.timing.navigationStart")
        dom_complete = driver.execute_script(
            "return window.performance.timing.domComplete")
        first_byte = driver.execute_script(
            "return window.performance.timing.responseStart")
        total_time = dom_complete - navigation_start
        first_byte_time = first_byte - navigation_start

        return total_time, first_byte_time

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

    def save(self, commit=True):
        print("save")
        try:
            print(self.cleaned_data['path'])
            total_time, first_byte_time = self.time_url(self.driver, self.cleaned_data['path'])
            print(total_time)
            print(first_byte_time)

        finally:
            site = Site()
            site.title = self.driver.title
            site.path = self.cleaned_data['path']
            site.dom = total_time
            site.first_byte = first_byte_time
            site.save()
            self.driver.close()
            return site

        return -1


    class Meta:
        model = Site
        fields = ["path", "dom", "first_byte"]