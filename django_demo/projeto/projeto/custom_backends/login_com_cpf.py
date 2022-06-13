from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

from usuarios.models import Usuario


class LoginComCPF(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            usuario = Usuario.objects.get(cpf=username.strip().lower())
        except Exception as e:
            return None 
        else:
            if usuario.user.check_password(password):
                return usuario.user

        return None


    def get_user(self,user_id):
        try:
            return User.objects.get(pk=user_id)
        except Exception as e:
            return None
