from __future__ import unicode_literals

import uuid

from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class NewUser(AbstractUser):
    profile = models.CharField('Profile', default='', max_length=256)

    def __str__(self):
        return unicode(self.id)

    def __unicode__(self):
        return unicode(self.id)

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')


@python_2_unicode_compatible
class RentPost(models.Model):
    def __str__(self):
        return self.id
    def __unicode__(self):
        return self.id

    house_status = (
        ('a', 'available'),
        ('r', 'rented'),
    )

    bedroom_num = (
        ('0', '0 bedroom'),
        ('1', '1 bedroom'),
        ('2', '2 bedroom'),
        ('3', '3 bedroom'),
        ('4+', '4+ bedroom'),
    )

    bathroom_num = (
        ('0', '0 bathroom'),
        ('1', '1 bathroom'),
        ('2', '2 bathroom'),
        ('3+', '3+ bedroom'),
    )

    rentway = (
        ('e', 'entire house'),
        ('p', 'private room'),
    )

    type = (
        ('a', 'house'),
        ('h', 'apartment'),
    )

    post_status = models.CharField(
        max_length=1,
        choices=house_status,
        default='a',
    )
    post_bedroom = models.CharField(
        max_length=2,
        choices=bedroom_num,
        default='0',
    )
    post_bathroom = models.CharField(
        max_length=2,
        choices=bathroom_num,
        default='0',
    )

    post_rentway = models.CharField(
        max_length=1,
        choices=rentway,
        default='e',
    )

    post_type = models.CharField(
        max_length=1,
        choices=type,
        default='a',
    )

    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    post_content = models.TextField()
    post_time = models.DateField()
    post_title = models.CharField(default='', max_length=256)

    #photo list
    photo_list = models.TextField()

    # Apartment Information
    post_price = models.IntegerField()

    post_address = models.CharField(max_length=256)
    post_available_time = models.DateField()

    # pet_policy
    post_cat_allowed = models.BooleanField(default=False)
    post_dog_allowed = models.BooleanField(default=False)

    # amenity
    post_gym = models.BooleanField(default=False)
    post_pool = models.BooleanField(default=False)
    post_wechat = models.CharField(max_length=256)
    post_phone = models.CharField(max_length=20)

@python_2_unicode_compatible
class UserPost(models.Model):
    def __str__(self):
        return self.id
    def __unicode__(self):
        return self.id

    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    post = models.ForeignKey(RentPost, on_delete=models.CASCADE)
