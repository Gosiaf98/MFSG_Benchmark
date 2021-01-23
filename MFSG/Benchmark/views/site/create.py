from django.views.generic.edit import CreateView
from .form import Form
from ...models import Site
from django.shortcuts import render
import matplotlib
matplotlib.use('Agg') #<= this is required
from matplotlib import pyplot as plt
import io
import urllib, base64
from pylab import *

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
            if form.cleaned_data['interactive']:
                data['interactive'] = site.interactive

        else:
            data['compare'] = True

            i = 11
            figLen = 0
            if form.cleaned_data['dom']:
                i += 100
                figLen += 5
            if form.cleaned_data['first_byte']:
                i += 100
                figLen += 5
            if form.cleaned_data['interactive']:
                i += 100
                figLen += 5

            fig = plt.figure(figsize=(10, figLen))

            ax = plt.subplot(i)
            x = np.arange(len(form.cleaned_data['compare_sites']) + 1)

            colors = ['orange', 'green', 'blue', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']

            if form.cleaned_data['first_byte']:
                titles = []
                first_bytes = []

                titles.append(site.title)
                first_bytes.append(site.first_byte)
                for c_site in form.cleaned_data['compare_sites']:
                    titles.append(c_site.title)
                    first_bytes.append(c_site.first_byte)
                bar = plt.bar(x, first_bytes, color=colors)
                plt.xticks([])
                plt.title("Time to First Byte")
                plt.ylabel('Czas [ms]')

                for rect in bar:
                    height = rect.get_height()
                    plt.text(rect.get_x() + rect.get_width() / 2.0, height, '%d' % int(height), ha='center', va='bottom')

                i += 1


            if form.cleaned_data['interactive']:
                titles = []
                interactives = []

                titles.append(site.title)
                interactives.append(site.interactive)
                for c_site in form.cleaned_data['compare_sites']:
                    titles.append(c_site.title)
                    interactives.append(c_site.interactive)
                plt.subplot(i)
                bar = plt.bar(x, interactives, color=colors)
                plt.xticks([])
                plt.title("Time to Interactive")
                plt.ylabel('Czas [ms]')

                for rect in bar:
                    height = rect.get_height()
                    plt.text(rect.get_x() + rect.get_width() / 2.0, height, '%d' % int(height), ha='center', va='bottom')


                i += 1

            if form.cleaned_data['dom']:
                titles = []
                doms = []

                titles.append(site.title)
                doms.append(site.dom)
                for c_site in form.cleaned_data['compare_sites']:
                    titles.append(c_site.title)
                    doms.append(c_site.dom)
                plt.subplot(i)
                bar = plt.bar(x, doms, color=colors)
                plt.xticks([])
                plt.title("DOM Complete Time")
                plt.ylabel('Czas [ms]')

                for rect in bar:
                    height = rect.get_height()
                    plt.text(rect.get_x() + rect.get_width() / 2.0, height, '%d' % int(height), ha='center', va='bottom')

            figlegend((bar), titles, bbox_to_anchor=(0.1, 0.92, 0.8, .102), loc='lower left', mode="expand",
                      borderaxespad=0.)

            buf = io.StringIO()
            fig.savefig(buf, format='svg', bbox_inches='tight')
            buf.seek(0)

            uri = buf.getvalue()

            data['uri'] = uri

            plt.close()


        return render(request, 'results.html', data)
