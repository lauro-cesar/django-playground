from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import os 
import sys
import re
from string import Template
from ._models import ALL_MODELS

TEMPLATES=[
    "actions.html",
    "admin_sidebar.html"]

class Command(BaseCommand):
    help = 'Create admin templates'    
                    

    def handle(self, *args, **options):
        for c in ALL_MODELS:
            app_name = c.__module__.split(".")[0]
 
            app_templates_dir = f"{settings.BASE_DIR}/templates/admin/{app_name}/{c.__name__.lower()}"



            if not os.path.exists(f"{app_templates_dir}"):
                self.stdout.write(f"criando: {app_templates_dir}")
                os.makedirs(app_templates_dir)    







        self.stdout.write(self.style.SUCCESS('Successfully'))