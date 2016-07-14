from django.contrib import admin

# Register your models here.
from data_processor.models import ServiceDescription, ViewingServices

admin.site.register(ServiceDescription)
admin.site.register(ViewingServices)
