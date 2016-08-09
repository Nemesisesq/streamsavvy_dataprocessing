import django
from django.db import models
from jsonfield import JSONField

class ModuleDescriptions(models.Model):
    level = models.TextField(blank=True, null=True)
    level_description = models.TextField(blank=True, null=True)
    service = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    networks = JSONField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    img = models.TextField(blank=True, null=True)
    affiliate_link = models.TextField(blank=True, null=True)

class ServiceDescription(models.Model):
    name = models.TextField(blank=True, null=True)
    slug = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    subscription_link = models.TextField(blank=True, null=True)
    google_play_link = models.TextField(blank=True, null=True)
    ios_appstore_link = models.TextField(blank=True, null=True)
    viewing_windows = models.TextField(blank=True, null=True)
    tooltip_tile_link = models.TextField(blank=True, null=True)

    def __str__(self):
        return("Service Description for {}".format(self.name))

class ViewingServices(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    windows =JSONField(blank=True, null=True)
    price = models.TextField(blank=True, null=True)
    ppv = models.BooleanField(default=False)




class Channel(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    guidebox_data = JSONField(blank=True, null=True)
    is_on_sling = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        managed = False
        db_table = 'server_channel'

    def __str__(self):
        return "{}".format(self.name)


class Content(models.Model):
    title = models.CharField(max_length=250, default='')
    guidebox_data = JSONField(default="")  # This field type is a guess.
    modified = models.DateTimeField()
    on_netflix = models.BooleanField()
    channels_last_checked = models.DateTimeField(blank=True, null=True)
    channel = models.ManyToManyField(Channel, blank=True)

    class Meta:
        managed = False
        db_table = 'server_content'

    def __str__(self):
        return "{0}".format(self.title)

    def get_tags(self):
        if 'detail' in self.guidebox_data:
            return [i['tag'] for i in self.guidebox_data['detail']['tags']]
        return []

    def get_genre(self):
        if 'detail' in self.guidebox_data:
            return [i['title'] for i in self.guidebox_data['detail']['genres']]
        return []

    def get_cast(self):
        if 'detail' in self.guidebox_data:
            return [i['name'] for i in self.guidebox_data['detail']['cast']]
        return []

class Sport(models.Model):
    category = models.TextField()
    title = models.TextField()
    json_data = JSONField(default="")
    date_created = models.DateTimeField(default=django.utils.timezone.now())


    def __str__(self):
        return "{0}".format(self.title)
