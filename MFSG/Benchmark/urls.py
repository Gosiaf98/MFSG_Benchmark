from django.urls import path
from .views import site

urlpatterns = [
    path('', site.Create.as_view(), name='site_create')
]
