from django.urls import path
from .views import UserProfileAPI, ReferralListAPI



app_name = 'auth_app'
urlpatterns = [
    path('profile/', UserProfileAPI.as_view(), name='api_user_profile'),
    path('referral_list/', ReferralListAPI.as_view(), name='api_referral_list'),
]