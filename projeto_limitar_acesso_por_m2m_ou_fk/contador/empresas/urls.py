from django.urls import path,include
from empresas.views import ListaDeEmpresas


urlpatterns = [
    path("lista/",ListaDeEmpresas.as_view(), name="empresas-list")
]

