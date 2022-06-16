from django.conf import settings
from django.urls import path, include

from usuarios.views import DetalhesDoUsuario


urlpatterns = [
    path("detalhe/<int:pk>/",DetalhesDoUsuario.as_view(),name="usuario-detail")
]

