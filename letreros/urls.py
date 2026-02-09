from django.urls import path

from .views import cotizar_api, inicio

urlpatterns = [
    path("", inicio, name="inicio"),
    path("api/cotizar/", cotizar_api, name="cotizar_api"),
]
