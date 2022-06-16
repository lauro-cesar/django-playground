from django.shortcuts import render
from projeto.base_views import UsuarioPrecisaEstarLogado
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from usuarios.models import Usuario



class DetalhesDoUsuario(UsuarioPrecisaEstarLogado,DetailView):
    template_name ="usuarios/usuario_detail.html"
    model = Usuario

