from django.contrib import admin

# Register your models here.
from data_processor.models import ServiceDescription, ViewingServices, ModuleDescriptions, Sport

admin.site.register(ServiceDescription)
admin.site.register(ViewingServices)
admin.site.register(ModuleDescriptions)
admin.site.register(Sport)
