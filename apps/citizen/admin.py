from django.contrib import admin
from .models import Citizen

# Register your models here.
#regions
class CitizenAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'id_number', 'dob', 'village', 'hamlet']
    search_fields = ['name__startwith']
    ordering = ("id",)

admin.site.register(Citizen, CitizenAdmin)
