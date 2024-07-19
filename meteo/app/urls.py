from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.Index.as_view(), name="index"),  # стартовая страница
    path('<str:city>/', views.GetMeteo.as_view(), name="get_meteo"),  # прогноз погоды по переданному городу

]
