"""
Django base views for class based resources
"""
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin



class UsuarioPrecisaEstarLogado(LoginRequiredMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "usuario":self.request.user
        })
        return context

