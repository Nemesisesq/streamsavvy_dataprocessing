from datetime import datetime

import django
from django.conf import settings
from django.contrib.auth.models import User, UserManager
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException

class EmailRequired(APIException):
    status_code = 500
    default_detail = 'Email is required'

class EmailNotUnique(APIException):
    status_code = 500
    default_detail = 'A user with this email already exists'

@receiver(pre_save, sender=User)
def User_pre_save(sender, **kwargs):
    email = kwargs['instance'].email
    username = kwargs['instance'].username

    if not email: raise EmailRequired()

    if sender.objects.filter(email=email).exclude(username=username).count() > 1:
        raise EmailNotUnique()

class AnonymousUser(User):
    session = models.TextField(blank=True, null=True)
    objects = UserManager()

    def is_authenticated(self):
        return False

    def __str__(self):
        return "{}".format(self.username)


class Profile(models.Model):
    device_id = JSONField(blank=True, null=True)
    user = models.OneToOneField(User, null=True)

class Images(models.Model):
    image_url = models.URLField(blank=True, null=True)
    thumbnail_small = models.URLField(blank=True, null=True)
    thumbnail_medium = models.URLField(blank=True, null=True)
    thumbnail_large = models.URLField(blank=True, null=True)
    thumbnail_x_large = models.URLField(blank=True, null=True)
    misc_pictures = models.TextField(blank=True, null=True)


class Price(models.Model):
    retail_cost = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    member_cost = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    subscription_monthly = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)


class Hardware(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    version = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    home_url = models.URLField(blank=True, null=True)
    price = models.ForeignKey(Price, blank=True, null=True)
    images = models.ForeignKey(Images, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return "{0} version {1}".format(self.name, self.version)


class Channel(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    guidebox_data = JSONField(blank=True, null=True)
    is_on_sling = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True, blank=True)

    def save(self, *args, **kwargs):
        self.modified = timezone.now()
        return super(Channel, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.name)


class Content(models.Model):
    title = models.CharField(max_length=250, blank=True, null=True)
    guidebox_data = JSONField(blank=True, null=True)
    on_netflix = models.BooleanField(default=False)
    channel = models.ManyToManyField(Channel, blank=True)
    modified = models.DateTimeField(auto_now=True, blank=True)
    channels_last_checked = models.DateTimeField(blank=True, null=True)
    curr_pop_score = models.FloatField(default=0.1)


    def save(self, *args, **kwargs):
        self.modified = timezone.now()
        return super(Content, self).save(*args, **kwargs)

    def __str__(self):
        return "Show {0}".format(self.title)


class Package(models.Model):
    owner = models.OneToOneField(User, related_name='packages')
    data = JSONField(blank=True, null=True, default={'content': [], 'services': [], 'hardware': []})
    modified = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return "Package Configuration {0} for {1}".format(self.pk, self.owner.username)

    def is_blank(self):
        return len(self.data['content']) > 0


class Feedback(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    data = JSONField(blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True)


class ChannelImages(models.Model):
    guidebox_id = models.TextField(blank=True, null=True, unique=True)
    data = JSONField(blank=True, null=True)

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)

class Popularity(models.Model):
    score = models.FloatField(default=0.1)
    date_created = models.DateField(default=django.utils.timezone.now())
    content = models.ForeignKey(Content)

    class Meta:
        managed=False
        db_table='popularity_popularity'
        get_latest_by = 'date_created'
