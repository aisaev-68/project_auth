from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'authorized', 'activation_code', 'invite_code', 'referrer')
