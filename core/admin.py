from django.contrib import admin  # type: ignore # I'm importing the admin module from Django's contrib package
from .models import Collaborator  # I'm importing the Colaborator model from the current directory's models module

# Register your models here.
admin.site.register(Collaborator)  # I'm registering the Colaborator model with Django's admin site
