"""
"""


APP_URLS_TEMPLATE ="""
from django.urls import path,include, re_path
from {{app_name|lower}}.views import {{model_name}}TemplateView,{{model_name}}DetailView, {{model_name}}ListView, {{model_name}}UpdateView, {{model_name}}DeleteView, {{model_name}}CreateView

urlpatterns = [    
    path("", {{model_name}}TemplateView.as_view(template_name="{{model_name|lower}}/app_templates/{{model_name|lower}}_index.html"), name="{{model_name|lower}}-index"),    
    path("collection/", {{model_name}}ListView.as_view(template_name = "{{model_name|lower}}/app_templates/{{model_name|lower}}_list.html"), name="{{model_name|lower}}-list"),
    path("collection/<int:pk>/", {{model_name}}DetailView.as_view(template_name = "{{model_name|lower}}/app_templates/{{model_name|lower}}_detail.html"), name='{{model_name|lower}}-detail'),
    path("collection/<int:pk>/editar/", {{model_name}}UpdateView.as_view(template_name = "{{model_name|lower}}/app_templates/{{model_name|lower}}_update.html"), name='{{model_name|lower}}-update'),
    path("collection/<int:pk>/remover/", {{model_name}}DeleteView.as_view(template_name = "{{model_name|lower}}/app_templates/{{model_name|lower}}_delete.html"), name='{{model_name|lower}}-delete'),    
    path("collection/adicionar/", {{model_name}}CreateView.as_view(template_name = "{{model_name|lower}}/app_templates/{{model_name|lower}}_create.html"), name='{{model_name|lower}}-create'),
]
"""
APP_URLS_INIT_TEMPLATE = """ """

URLS_TEMPLATE = """
from django.urls import path,include, re_path
from {{app_name|lower}}.views import {{model_name}}TemplateView,{{model_name}}DetailView, {{model_name}}ListView, {{model_name}}UpdateView, {{model_name}}DeleteView, {{model_name}}CreateView

urlpatterns = [    
    path("", {{model_name}}TemplateView.as_view(), name="{{model_name|lower}}-index"),    
    path("collection/", {{model_name}}ListView.as_view(), name="{{model_name|lower}}-list"),
    path("collection/<int:pk>/", {{model_name}}DetailView.as_view(), name='{{model_name|lower}}-detail'),
    path("collection/<int:pk>/editar/", {{model_name}}UpdateView.as_view(), name='{{model_name|lower}}-update'),
    path("collection/<int:pk>/remover/", {{model_name}}DeleteView.as_view(), name='{{model_name|lower}}-delete'),    
    path("collection/adicionar/", {{model_name}}CreateView.as_view(), name='{{model_name|lower}}-create'),
]
"""

URLS_INIT_TEMPLATE = """ """

CHANNELS_TEMPLATE = """
import logging
logger = logging.getLogger(__name__)
import hashlib
import json
from project.celery_tasks import app
from asgiref.sync import sync_to_async
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer,AsyncJsonWebsocketConsumer
from {{app_name}}.models import {{model_name}}


class {{model_name}}CollectionConsumer(AsyncJsonWebsocketConsumer):
    model_meta = {{model_name}}._meta
    

    @property
    def nome_do_grupo(self):
        return f"{{app_name}}_collection_{{model_name|lower}}"

    @property
    def groupID(self):
        return hashlib.md5(self.nome_do_grupo.encode("utf-8")).hexdigest()

    def can_view(self):
        self.user = self.scope["user"]        
        if self.user.is_authenticated:
            return self.user.has_perm(f"{self.model_meta.app_label}.view_{self.model_meta.model_name}")
        return False

    async def connect(self):
        self.user = self.scope["user"]        
        if self.user.is_authenticated:
            can_view = await sync_to_async(self.can_view)()
            if can_view:                             
                await self.channel_layer.group_add(self.nome_do_grupo, self.channel_name)        
                await self.accept()
        else:
            await self.close()


    async def disconnect(self, close_code):       
        pass

    async def receive_json(self, content):     
        await self.channel_layer.group_send(
            self.nome_do_grupo, {"type": "group_message", "content": content}
        )

    async def group_message(self, event):                    
        message = event["content"]
        await self.send_json(message)

    async def receive(self, text_data):
        await self.send(text_data=text_data)



class {{model_name}}Consumer(AsyncJsonWebsocketConsumer):
    object_pk =-1
    model_meta = {{model_name}}._meta
    
    @property
    def nome_do_grupo(self):
        return f"{{model_name}}_{self.object_pk}" 

    @property
    def groupID(self):
        return hashlib.md5(self.nome_do_grupo.encode("utf-8")).hexdigest()

    def can_view(self):
        self.user = self.scope["user"]        
        if self.user.is_authenticated:
            return self.user.has_perm(f"{self.model_meta.app_label}.view_{self.model_meta.model_name}")
        return False

    async def connect(self):
        self.user = self.scope["user"]        
        if self.user.is_authenticated:
            can_view = await sync_to_async(self.can_view)()
            if can_view:                
                url_route = self.scope.get("url_route",{})
                route_kwargs = url_route.get("kwargs",{})
                self.object_pk =route_kwargs.get("object_pk","-1")
                await self.channel_layer.group_add(self.nome_do_grupo, self.channel_name)        
                await self.accept()
                app.send_task("{{STREAM_OBJECT_TASK_NAME}}",[self.object_pk])
        else:
            await self.close()


    async def disconnect(self, close_code):       
        pass

    async def receive_json(self, content):     
        await self.channel_layer.group_send(
            self.nome_do_grupo, {"type": "group_message", "content": content}
        )

    async def group_message(self, event):                    
        message = event["content"]
        await self.send_json(message)

    async def receive(self, text_data):
        await self.send(text_data=text_data)

"""




CHANNELS_INIT_TEMPLATE ="""\nfrom .{{save_to}} import {{model_name}}Consumer\n"""

SERIALIZER_INIT_TEMPLATE ="""\nfrom .{{save_to}} import {{model_name}}Serializer\n"""

SERIALIZER_TEMPLATE = """
from rest_framework import serializers
from {{app_name}}.models import {{model_name}}

class {{model_name}}Serializer(serializers.ModelSerializer):   
    def create(self, validated_data):        
        criado_por = self.context.get('criado_por',None)
        if criado_por:
            validated_data.update({
                'criado_por':criado_por
            })
            
        instance = {{model_name}}.objects.create(**validated_data)       
        return instance

    class Meta:
        model = {{model_name}}
        fields = {{model_name}}.SERIALIZABLES
        if {{model_name}}.READ_ONLY_FIELDS:
            read_only_fields ={{model_name}}.READ_ONLY_FIELDS

"""


VIEW_INIT_TEMPLATE ="""\nfrom .{{save_to}} import {{model_name}}TemplateView, {{model_name}}ViewSet, {{model_name}}DetailView, {{model_name}}ListView, {{model_name}}UpdateView, {{model_name}}CreateView, {{model_name}}DeleteView\n"""


VIEW_TEMPLATE = """
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from project.authentication import APITokenAuthentication
from django.views.generic import View
from django.http import JsonResponse
from django.middleware import csrf
from django.db import IntegrityError
from django.core.exceptions import ValidationError
import json
import re
from django.urls import reverse_lazy
from django.core.cache import cache
from django.utils.safestring import mark_safe
from project.celery_tasks import app
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sites.shortcuts import get_current_site
from project.views import BaseTemplateView
from {{app_name}}.serializers import {{model_name}}Serializer
from {{app_name}}.models import {{model_name}}
from project.views import CustomBaseListView, CustomBaseDetailView, CustomBaseUpdateView, CustomBaseCreateView, CustomBaseDeleteView



class {{model_name}}DeleteView(CustomBaseDeleteView):
    template_name = "{{model_name|lower}}/{{model_name|lower}}_delete.html"
    model = {{model_name}}
    success_url = reverse_lazy('{{model_name|lower}}-list')
 
    @method_decorator(login_required)
    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        self.user = self.request.user
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)      
        context.update(
            {
            "user":self.user
            })
        context.update(self.common_context())
        return context



class {{model_name}}CreateView(CustomBaseCreateView):
    template_name = "{{model_name|lower}}/{{model_name|lower}}_create.html"
    model = {{model_name}}
    fields = {{model_name}}.CREATE_FIELDS
    success_url = reverse_lazy('{{model_name|lower}}-list')
 
    @method_decorator(login_required)
    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        self.user = self.request.user
        if self.next:           
            self.success_url = self.next     
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)      
        context.update(
            {
            "user":self.user
            })
        context.update(self.common_context())
        return context



class {{model_name}}UpdateView(CustomBaseUpdateView):
    template_name = "{{model_name|lower}}/{{model_name|lower}}_update.html"
    model = {{model_name}}
    fields = {{model_name}}.CREATE_FIELDS
 
    @method_decorator(login_required)
    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        self.user = self.request.user
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)      
        context.update(
            {
            "user":self.user
            })
        context.update(self.common_context())
        return context



class {{model_name}}DetailView(CustomBaseDetailView):
    template_name = "{{model_name|lower}}/{{model_name|lower}}_detail.html"
    model = {{model_name}}
 
    @method_decorator(login_required)
    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        self.user = self.request.user
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)      
        context.update(
            {
            "user":self.user
            })
        context.update(self.common_context())
        return context



class {{model_name}}ListView(CustomBaseListView):
    template_name = "{{model_name|lower}}/{{model_name|lower}}_list.html"
    model = {{model_name}}
    paginate_by = 15
    allow_empty = True
    
    @method_decorator(login_required)
    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        self.user = self.request.user
        return super().dispatch(*args, **kwargs)


    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)   
        context.update(
            {
            "user":self.user
            })
        context.update(self.common_context())
        return context




class {{model_name}}TemplateView(BaseTemplateView):
    template_name = "{{model_name|lower}}/{{model_name|lower}}_base.html"

    @method_decorator(login_required)
    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        self.user = self.request.user
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)      
        context.update(
            {
            "body_class":"manager",
            "user":self.user
            })
        context.update(self.common_context())
        return context




class {{model_name}}ViewSet(viewsets.ModelViewSet):
   serializer_class = {{model_name}}Serializer
   permission_classes = [IsAuthenticated]
   authentication_classes = [SessionAuthentication, APITokenAuthentication]
   parser_classes = [JSONParser]

   def get_serializer_context(self):       
       return {
           "criado_por":self.request.user,         
           "request": self.request,  # request object is passed here
           "format": self.format_kwarg,
           "view": self,
       }

   def get_queryset(self):        
       return {{model_name}}.objects.filter(isActive=True)

"""

TASK_INIT_TEMPLATE ="""\nfrom . import {{save_to}}\n"""

TASK_TEMPLATE = """
import logging
logger = logging.getLogger(__name__)
from celery import shared_task
from django.conf import settings
from django.utils.encoding import smart_str
from PIL import Image, ImageOps, ImageDraw,ImageFont
from io import BytesIO
from django.core.cache import cache
from django.utils.text import slugify
import json
from django.urls import reverse_lazy
import base64
from project.celery_tasks import app
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from {{app_name}}.models import {{model_name}}
from {{app_name}}.serializers import {{model_name}}Serializer




@shared_task(name="{{STREAM_COLLECTION_TASK_NAME}}", max_retries=2, soft_time_limit=45)
def on_{{STREAM_COLLECTION_TASK_NAME}}_task(object_pk):
    logger.debug(f"sending live update {object_pk}")
    instance = {{model_name}}.get_or_none(pk=object_pk)
    if instance:
        channel_layer = get_channel_layer()        
        try:                        
            serializador = {{model_name}}Serializer(instance)
            async_to_sync(channel_layer.group_send)(
               f"{{app_name}}_collection_{{model_name|lower}}", {"type": "group_message", "content": serializador.data}
            )
        except Exception as e:           
            logger.error(e.__repr__())           
    else:
        logger.debug(f"Nao achei {object_pk}")



@shared_task(name="{{STREAM_OBJECT_TASK_NAME}}", max_retries=2, soft_time_limit=45)
def on_{{STREAM_OBJECT_TASK_NAME}}_task(object_pk):
    instance = {{model_name}}.get_or_none(pk=object_pk)
    if instance:
        channel_layer = get_channel_layer()        
        try:                        
            serializador = {{model_name}}Serializer(instance)
            async_to_sync(channel_layer.group_send)(
                f"{{model_name}}_{object_pk}", {"type": "group_message", "content": serializador.data}
            )
        except Exception as e:           
            print(e.__repr__())
"""


SIGNAL_INIT_TEMPLATE ="""\nfrom .{{save_to}}  import  PostSave{{model_name}}Signals\n"""


SIGNAL_TEMPLATE ="""
from django.db.models.signals import (
    pre_save,
    post_save,
    pre_init,
    post_init,
    pre_delete,
    post_delete,
    m2m_changed,
)

import hashlib
from django.dispatch import receiver
from django.conf import settings
from project.celery_tasks import app
from {{app_name}}.models import {{model_name}}


@receiver(post_save, sender={{model_name}})
def PostSave{{model_name}}Signals(
    sender, instance, created, using, update_fields, *args, **kwargs
):
    if True in [created]:
        for task in {{model_name}}.TASKS.get('on_create',[]):
            app.send_task(task, [instance.id])
    else:
        for task in {{model_name}}.TASKS.get('on_save',[]):
            app.send_task(task, [instance.id])
"""


MODEL_INIT_TEMPLATE ="""\nfrom .{{save_to}} import {{model_name}}\n"""

MODEL_TEMPLATE = """
import logging
logger = logging.getLogger(__name__)
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import smart_str
from django.conf import settings
import base64
from django.urls import reverse
from django.core.cache import cache
from django.utils.safestring import mark_safe
from project.celery_tasks import app
from django.contrib import messages
from project.models import BaseModel, StackedModel



class {{model_name}}(BaseModel):
    SERIALIZABLES =['id','label']
    READ_ONLY_FIELDS=[]
    ADMIN_LIST_EDITABLE=[]
    ADMIN_LIST_DISPLAY=['label']
    ADMIN_ORDERING=[]
    ADMIN_FILTER_HORIZONTAL= []
    ADMIN_LIST_FILTER=[]
    ADMIN_SEARCH_FILTER=[]
    ADMIN_DISPLAY_LINKS=['label']
    EXCLUDE_FROM_ADMIN=[]
    CREATE_FIELDS=[]
    FORM_FIELDS=[]
 
    TASKS={
        'on_create':["{{STREAM_COLLECTION_TASK_NAME}}"],
        'on_save':["{{STREAM_OBJECT_TASK_NAME}}"],
        'on_delete':[]
    }

    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL,
        null=True, blank=True, on_delete=models.SET_NULL,related_name="{{model_name|lower}}_criados_por_mim")

    modificado_por = models.ForeignKey(settings.AUTH_USER_MODEL,null=True ,blank=True, on_delete=models.SET_NULL,related_name="{{model_name|lower}}_modificados_por_mim")

    removido_por = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, on_delete=models.SET_NULL,related_name="{{model_name|lower}}_removidos_por_mim")

    def get_list_url(self):
        return reverse('{{model_name|lower}}-list')

    def get_absolute_url(self):
        return reverse('{{model_name|lower}}-detail', args=[str(self.id)])
    
    def get_delete_url(self):
        return reverse('{{model_name|lower}}-delete', args=[str(self.id)])

    def get_detail_url(self):
        return reverse('{{model_name|lower}}-detail', args=[str(self.id)])
    
    def get_create_url(self):
        return reverse('{{model_name|lower}}-create')

    def get_update_url(self):
        return reverse('{{model_name|lower}}-update', args=[str(self.id)])


    @property
    def label(self):
        return "{{verbose_name}}"

    class Meta(BaseModel.Meta):
        verbose_name = _("{{verbose_name}}")
        verbose_name_plural = _("{{verbose_name_plural}}")

    def __str__(self):
        return self.label

"""

ADMIN_INIT_TEMPLATE ="""\nfrom .{{save_to}} import {{model_name}}Admin\n"""

ADMIN_TEMPLATE = """
from django.contrib import admin
from django.core.cache import cache
from django.utils.safestring import mark_safe
from project.celery_tasks import app
from django.contrib import messages
import base64
from django.utils.translation import gettext_lazy as _
from project.admin import BaseModelAdmin
from {{app_name}}.models import {{model_name}}
from project.admin import project_dashboard_site

@admin.register({{model_name}})
class {{model_name}}Admin(BaseModelAdmin):
    save_on_top = True
    ordering = {{model_name}}.ADMIN_ORDERING
    list_display = {{model_name}}.ADMIN_LIST_DISPLAY
    list_filter = {{model_name}}.ADMIN_LIST_FILTER
    search_fields = {{model_name}}.ADMIN_SEARCH_FILTER
    list_editable = {{model_name}}.ADMIN_LIST_EDITABLE
    list_display_links={{model_name}}.ADMIN_DISPLAY_LINKS
    filter_horizontal= {{model_name}}.ADMIN_FILTER_HORIZONTAL
    exclude = BaseModelAdmin.exclude + {{model_name}}.EXCLUDE_FROM_ADMIN
    actions=['{{STREAM_OBJECT_TASK_NAME}}']

    def {{STREAM_OBJECT_TASK_NAME}}(self, request, queryset):
        for obj in queryset:
            try:
                result =  app.send_task("{{STREAM_OBJECT_TASK_NAME}}",[obj.id])
            except Exception as e:
                self.message_user(
                    request,
                    f"{obj.label}: {e.__repr__()}",
                    messages.ERROR,
                )
            else:
                self.message_user(
                    request,
                    "{label}: enviado para a fila de processamento".format(label=obj),
                    messages.SUCCESS,
                )

    {{STREAM_OBJECT_TASK_NAME}}.short_description = _("Send to stream")
    {{STREAM_OBJECT_TASK_NAME}}.allowed_permissions = ['{{STREAM_OBJECT_TASK_NAME}}']

    def has_{{STREAM_OBJECT_TASK_NAME}}_permission(self,request, obj=None):
        return request.user.is_superuser  



    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

project_dashboard_site.register({{model_name}},{{model_name}}Admin)

"""