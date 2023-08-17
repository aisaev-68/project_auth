from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login

import random
import string
import time
from .models import UserProfile
from .serializers import UserProfileSerializer

def generate_invite_code():
    characters = string.digits + string.ascii_uppercase
    return ''.join(random.choice(characters) for _ in range(6))


class AuthorizationPhoneView(View):
    template_name = 'auth_app/authorize_phone.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        phone_number = request.POST.get('phone_number')

        # Имитация задержки отправки SMS
        time.sleep(2)

        activation_code = ''.join(random.choices(string.digits, k=4))  # Генерация случайного кода
        invite_code = generate_invite_code()
        user, created = UserProfile.objects.get_or_create(phone_number=phone_number)
        if created:
            user.invite_code = invite_code
            user.activation_code = activation_code
            user.save()

        request.session['phone_number'] = phone_number
        request.session['activation_code'] = activation_code
        request.session['invite_code'] = invite_code

        return redirect('verify_code')


class VerifyCodeView(View):
    template_name = 'auth_app/verify_code.html'

    def get(self, request):
        return render(
            request,
            self.template_name,
            context={'activation_code': request.session['activation_code']}
        )

    def post(self, request):
        activation_code = request.POST.get('activation_code')
        phone_number = request.session.get('phone_number')

        user = UserProfile.objects.get(
            phone_number=phone_number,
        )

        if user and activation_code == request.session.get('activation_code'):
            user.authorized = True
            user.save()
            return redirect('auth_app:api_user_profile')
        return redirect('authorize_phone')


class UserProfileAPI(APIView):
    def get(self, request):
        phone_number = request.session.get('phone_number')
        try:
            user = UserProfile.objects.get(phone_number=phone_number)
            serializer = UserProfileSerializer(user)
            return render(request, 'auth_app/profile.html', {'user': serializer.data})
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)



class ReferralListAPI(APIView):
    def get(self, request):
        user = UserProfile.objects.get(phone_number=request.session['phone_number'])
        referred_users = user.referred_users.all()
        referred_phone_numbers = [user.phone_number for user in referred_users]
        return Response({'referred_users': referred_phone_numbers})


class InputInviteCodeView(View):
    template_name = 'auth_app/profile.html'

    def post(self, request):
        user = UserProfile.objects.get(phone_number=request.session.get('phone_number'))
        invite_code = request.POST.get('invite_code')
        try:
            invited_user = UserProfile.objects.get(invite_code=invite_code)
            user.referrer = invited_user
            user.invite_code = None  # Очистка собственного инвайт-кода пользователя
            user.save()
            user.referred_users.add(invited_user)
            return redirect('auth_app:api_user_profile')
        except UserProfile.DoesNotExist:
            return redirect('api_user_profile', error_message='Неверный инвайт-код')

