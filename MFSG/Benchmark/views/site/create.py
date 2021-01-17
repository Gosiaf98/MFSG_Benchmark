from django.views.generic.edit import CreateView
from .form import Form
from ...models import Site
from django.shortcuts import render


class Create(CreateView):
    template_name = "site_create.html"
    form_class = Form
    model = Site

    def form_valid(self, form):
        self.object = form.save()
        return self.results(self.request, self.object, form)

    def results(self, request, site, form):
        data = {'title': site.title}

        if not form.cleaned_data['compare_sites']:
            data['compare'] = False

            if form.cleaned_data['dom']:
                data['dom'] = site.dom
            if form.cleaned_data['first_byte']:
                data['first_byte'] = site.first_byte

        else:
            data['compare'] = True

        return render(request, 'results.html', data)
