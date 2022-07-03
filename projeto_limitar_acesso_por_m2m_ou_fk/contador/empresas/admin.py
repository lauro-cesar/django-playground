from django.contrib import admin
from django.utils.safestring import mark_safe
from empresas.models import Empresa


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    save_on_top = True 
    filter_horizontal = ['operadores']
    search_fields = ['operadores']
    list_display = ['id','total_operadores','logotipo_url']




    # def has_view_permission(self, request,obj=None):
    #     return True

    # def has_view_or_change_permission(self, request,obj=None):
    #     return True

    # def has_add_permission(self, request):
    #     return True

    # def has_delete_permission(self, request, obj=None):
    #     return True


    def logotipo_url(self, obj):  # receives the instance as an argument

        return mark_safe(
            '<img width=96px src="{url}" />'.format(
                url=obj.logotipo.url,
            )
        )
    
    logotipo_url.allow_tags = True
    logotipo_url.short_description = "Logotipo"

