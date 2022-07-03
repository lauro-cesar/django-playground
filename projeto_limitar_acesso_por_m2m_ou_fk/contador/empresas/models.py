"""
Modulo responsavel pelo modelo da empresa
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class Empresa(models.Model):
    """
    Classe que armazena info sobre a empresa e associacao com os operadores..
    """
    logotipo = models.ImageField(upload_to="icones/empresas")
    nome_da_empresa = models.CharField(max_length=512, verbose_name=_("Nome da empresa"), blank=True, default="Empresa")
    operadores = models.ManyToManyField(
        User,
        verbose_name="Operadores da empresa",
        related_query_name="minhas_empresas",
        related_name="minha_lista_de_empresas"
    )

    @property
    def total_operadores(self):
        return self.operadores.count()

