from django.urls import reverse
from django.views.generic.edit import FormView
from .form import Form
from ...models import Site


class Create(FormView):
    template_name = "site_create.html"
    form_class = Form
    model = Site
