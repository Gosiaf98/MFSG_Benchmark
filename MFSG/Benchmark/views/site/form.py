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
    dom = forms.BooleanField(required=False, label="DOM Complete Time", help_text="Czas, w którym strona i wszystkie jej zasoby podrzędne będą gotowe.")
    first_byte = forms.BooleanField(required=False, label="Time to First Byte", help_text="Wartość mierzona od momentu wysłania zapytania, do chwili otrzymania przez użytkownika pierwszego bajtu danych wysłanych przez serwer.")
    interactive = forms.BooleanField(required=False, label="Time to Interactive", help_text="Ilość czasu, jaki jest potrzebny, aby strona stała się w pełni interaktywna.")

    sites = Site.objects.all()

    compare_sites = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple, queryset=sites, label="<b>Wybierz strony, z którymi chcesz się porównać:</b>", required=False, help_text="Przytrzymaj CTRL, aby zaznaczyć więcej niż jedną stronę.")

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
        interactive = driver.execute_script(
            "return window.performance.timing.domInteractive")

        total_time = dom_complete - navigation_start
        first_byte_time = first_byte - navigation_start
        interactive_time = interactive - navigation_start

        return total_time, first_byte_time, interactive_time

    def clean_path(self):
        path = self.cleaned_data.get('path')

        try:
            self.driver.get(path)
        except:
            raise forms.ValidationError(
                self.error_messages['path_incorrect'],
                code='path_incorrect'
            )

        return path

    def clean(self):
        cleaned_data = super(Form, self).clean()

        dom = cleaned_data.get('dom')
        first_byte = cleaned_data.get('first_byte')
        interactive = cleaned_data.get('interactive')
        if not dom and not first_byte and not interactive:
            raise forms.ValidationError(
                self.error_messages['no_measure'],
                code='no_measure'
            )

        return cleaned_data

    def save(self, commit=True):
        print("save")
        try:
            total_time, first_byte_time, interactive_time = self.time_url(self.driver, self.cleaned_data['path'])

        finally:
            site = Site()
            site.title = self.driver.title
            site.path = self.cleaned_data['path']
            site.dom = total_time
            site.first_byte = first_byte_time
            site.interactive = interactive_time
            site.save()
            #self.driver.close()

            return site

        return -1


    class Meta:
        model = Site
        fields = ["path", "dom", "first_byte", "interactive"]