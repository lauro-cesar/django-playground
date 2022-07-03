from django.shortcuts import render
from contador.custom_views import RetornaListaDasMinhasEmpresas, UsuarioPrecisaEstarLogado
# Create your views here.
from django.views.generic.list import ListView
from empresas.models import Empresa


class ListaDeEmpresas(UsuarioPrecisaEstarLogado,ListView):
    template_name = "empresa/lista_de_empresas.html"
    model = Empresa
    paginate_by= 15
    allow_empty= True






    