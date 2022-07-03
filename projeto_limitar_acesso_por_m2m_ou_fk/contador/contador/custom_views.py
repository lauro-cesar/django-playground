from django.views.generic.base import View
from django.utils.functional import cached_property
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin



class RetornaListaDasMinhasEmpresas(View):

    @cached_property
    def listaDeEmpresas(self):
        """
        Retorna uma lista com os IDs da minhas empresas
        return [1,5,6]
        """
        return list(map(lambda empresa:empresa.id, self.request.user.minha_lista_de_empresas.all()))

class UsuarioPrecisaEstarLogado(LoginRequiredMixin,RetornaListaDasMinhasEmpresas):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "usuario":self.request.user,
            "minha_lista":self.listaDeEmpresas
        })
        return context


        
        
