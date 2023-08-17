from django.db import models
import random
import string


class UserProfile(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    authorized = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=4, null=True)
    invite_code = models.CharField(max_length=6, null=True, blank=True)
    referrer = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    referred_users = models.ManyToManyField('self', blank=True)



    def __str__(self):
        return self.phone_number

