from django.contrib import admin

# Register your models here.
from usuarios.models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    save_on_top= True 
    search_fields = ['cpf']
    list_filter = ['user__is_superuser']