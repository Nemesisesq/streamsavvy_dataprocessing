from django.contrib import admin

from server.models import *

# Register your models here.

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    pass


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    search_fields = ('name','is_on_sling')
    pass


@admin.register(Hardware)
class HardwareAdmin(admin.ModelAdmin):
    pass


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    pass

@admin.register(Feedback)
class Feedback(admin.ModelAdmin):
    pass

@admin.register(ChannelImages)
class ChannelImagesAdmin(admin.ModelAdmin):
    pass