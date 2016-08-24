from django.contrib.postgres.fields import JSONField
from django.db import models

# Create your models here.

class PostalCode(models.Model):
    zipcode = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.zipcode

class RoviListings(models.Model):
    service_id = models.TextField( blank=True, null=True)
    postal_code = models.TextField(blank=True, null=True)
    locale = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    data = JSONField(blank=True, null=True)

    def __str__(self):
        return self.service_id

class RoviGridSchedule(models.Model):
    listing = models.ForeignKey(RoviListings, null=True, blank=True)
    locale = models.TextField(blank=True, null=True)
    data = JSONField(blank=True, null=True)
    postal_code = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.data['GridScheduleResult']['Name']

class CallSigns(models.Model):
    callsign = models.TextField()
    network_affiliation = models.TextField()
    data = JSONField(blank=True, null=True)


class RoviProgramImages(models.Model):
    program_id  = models.TextField(blank=True, null=True)
    image_list = JSONField(blank=True, null=True)
