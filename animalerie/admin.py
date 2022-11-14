from django.contrib import admin
from .models import Animal
from .models import Equipement

# Register your models here.
admin.site.register(Animal)
admin.site.register(Equipement)
