from django.urls import reverse
from django.views.generic import CreateView
from .form import Form
from ...models import Site


class Create(CreateView):
    template_name = "site_create.html"
    form_class = Form
    model = Site
