from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse

# Create your views here.

from . import forms
from . import models
from . import get_meteo


class Index(View):
    """
    - на странице вводим через форму название города и перенаправляем на страницу с отработкой запроса
    """

    def get(self, request, *args, **kwargs):
        form = forms.City()
        template_name = "app/index.html"
        context = {'form': form}
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        form = forms.City(request.POST)  # Получаем данные формы из запроса
        if form.is_valid():  # Проверяем данные формы на корректность
            city = form.cleaned_data.get("city")
            return HttpResponseRedirect("{}/".format(city))


class GetMeteo(TemplateView):
    template_name = "app/get_meteo.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city = self.kwargs.get("city").lower()
        context['city'] = city
        temperature_now = get_meteo.Meteo(city=city)  # передали температуру
        if temperature_now:
            context['date'] = temperature_now
        else:
            context['date'] = None

        return context
