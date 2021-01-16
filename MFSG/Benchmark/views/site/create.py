from django.views.generic.edit import CreateView
from .form import Form
from ...models import Site
from django.shortcuts import render
from django.template import loader


class Create(CreateView):
    template_name = "site_create.html"
    form_class = Form
    model = Site

    def form_valid(self, form):
        self.object = form.save()
        return self.results(self.request, form)

    def results(self, request, form):
        print(form.cleaned_data['path'])
        template = loader.get_template('results.html')
        return render(request, 'results.html')
