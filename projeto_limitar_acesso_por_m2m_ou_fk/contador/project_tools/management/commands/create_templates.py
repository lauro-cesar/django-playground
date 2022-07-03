from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import os 
import sys
import re
from string import Template
from ._models import ALL_MODELS



class Command(BaseCommand):
    help = 'Create fields templates'    


    def create_templates(self,base_dir,model_name,verbose_name,template_suffix):
        render_context ={
            "model_name":model_name,
            "verbose_name":verbose_name
        }
        templates_source_dir = f"{settings.BASE_DIR}/templates/"
       
        TEMPLATES=["_base","_create","_delete","_detail","_list","_grid","_update","_form_create","_form_delete","_form_pesquisa","_form_update"]


        for t in TEMPLATES:
            template_source_in=""                        
            output=f"{base_dir}/{model_name}{t}.html"
            if not os.path.exists(output):     
                with open(f"{templates_source_dir}/{t}_{template_suffix}.html") as template_source:
                    template_source_in = template_source.read()
                with open(output,"w") as save_to_file:                    
                    template_output = Template(template_source_in).substitute(**render_context)
                    save_to_file.write(template_output)
                    save_to_file.close()

                    

    def handle(self, *args, **options):
        for c in ALL_MODELS:
            app_name = c.__module__.split(".")[0]
            web_templates_dir = f"{settings.BASE_DIR}/{app_name}/templates/{c.__name__.lower()}"

            app_templates_dir = f"{settings.BASE_DIR}/{app_name}/templates/{c.__name__.lower()}/app_templates/"
            
            fields_dir = f"{settings.BASE_DIR}/{app_name}/templates/{c.__name__.lower()}/fields/"
            
            
        
            if not os.path.exists(f"{fields_dir}"):
                os.makedirs(fields_dir)     

            if not os.path.exists(f"{app_templates_dir}"):
                os.makedirs(app_templates_dir)    


            self.create_templates(base_dir=web_templates_dir,model_name=c.__name__.lower(),verbose_name=c._meta.verbose_name,template_suffix="web")

            self.create_templates(base_dir=app_templates_dir,model_name=c.__name__.lower(),verbose_name=c._meta.verbose_name,template_suffix="app")


            campos = list( map( lambda f:f.name, c._meta.fields))
            for campo in campos:
                if not os.path.exists(f"{fields_dir}/{campo}.html"):                   
                    self.stdout.write( f"Criando: {fields_dir}/{campo}.html")

                    with open(f"{fields_dir}/{campo}.html","w") as save_to_file:
                        save_to_file.write("""{%% load i18n static project_tags%%}{%% spaceless %%}<div class="mb-4"><span class="field_form_errors">{{ form.%s.errors }}</span><label for="{{form.%s.id_for_label}}">{{form.%s.label}}{%% if form.%s.field.required %%}<span class="text-red m-2">*</span>{%% endif%%}</label>{{form.%s}}</div>{%% endspaceless %%}""" % (campo,campo,campo,campo,campo))
                        save_to_file.close()

        self.stdout.write(self.style.SUCCESS('Successfully'))