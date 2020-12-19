from django.shortcuts import render
from django.views.generic import TemplateView, ListView, UpdateView

# Create your views here.


class HomepageView(TemplateView):
    template_name = "dummygenerator/home.html"
    extra_context = {"title": "Home"}


class ListSchemas(ListView):
    pass


class EditSchemas(UpdateView):
    pass
