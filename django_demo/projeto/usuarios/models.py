from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()


class Usuario(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    cpf = models.CharField(max_length=32,verbose_name=_("CPF do usuário"), unique=True)


    class Meta:
        verbose_name = _("Usuário")
        verbose_name_plural = _("Usuários")

    def __str__(self):
        return self.user.get_full_name()


