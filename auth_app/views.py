from django.shortcuts import render, redirect
from django.views import View
import random
import string
import time

from .models import UserProfile


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

