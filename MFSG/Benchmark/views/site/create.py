from django.urls import reverse
from django.views.generic.edit import CreateView
from .form import Form
from ...models import Site


class Create(CreateView):
    template_name = "site_create.html"
    form_class = Form
    model = Site
    success_url = "/"

