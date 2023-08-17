from django.shortcuts import render, redirect
from django.views import View
import random
import string
import time

from .models import UserProfile


def generate_invite_code():
    """
    Генерирует случайный инвайт-код.
    Возвращает:
        str: Сгенерированный случайный инвайт-код.
    """
    characters = string.digits + string.ascii_uppercase
    return ''.join(random.choice(characters) for _ in range(6))


class AuthorizationPhoneView(View):
    """
    Обрабатывает авторизацию по номеру телефона.
    GET метод:
        Отображает форму для ввода номера телефона.
    POST метод:
        Обрабатывает отправку формы с номером телефона. Генерирует код
        активации, имитирует задержку отправки SMS, создает или обновляет
        профиль пользователя с указанным номером телефона и сгенерированными
        кодами активации и инвайта. Перенаправляет на страницу верификации.
    """
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
    """
    Обрабатывает верификацию кодов активации.
    GET метод:
        Отображает форму для ввода кода активации. Отображает код активации
        и список телефонных номеров, приглашенных пользователем.
    POST метод:
        Обрабатывает отправку формы с кодом активации. Сравнивает введенный
        код активации с сохраненным кодом. Если коды совпадают, помечает
        пользователя как авторизованного и отображает страницу профиля
        пользователя с списком телефонных номеров, приглашенных пользователем.
    """

    template_name = 'auth_app/verify_code.html'

    def get(self, request):
        user = UserProfile.objects.get(phone_number=request.session.get('phone_number'))
        referred_users = user.referred_users.all()
        referred_phone_numbers = [user.phone_number for user in referred_users]
        return render(
            request,
            self.template_name,
            context={
                'activation_code': request.session['activation_code'],
                'referred_phone_numbers': referred_phone_numbers
            }
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
            return render(request, 'auth_app/profile.html',
                          context={'user': user, 'referred_phone_numbers': user.referred_users.all()})
        return redirect('authorize_phone')


class InputInviteCodeView(View):
    """
    Обрабатывает ввод инвайт-кода приглашения.

    POST метод:
        Обрабатывает отправку формы с инвайт-кодом. Получает профиль пользователя
        и введенный инвайт-код. Если инвайт-код действителен, связывает
        пользователя с пригласившим пользователем, удаляет инвайт-код пользователя
        и добавляет пригласившего пользователя в список приглашенных. Перенаправляет
        на страницу профиля пользователя.
    """
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
            return redirect('profile')
        except UserProfile.DoesNotExist:
            return redirect('api_user_profile', error_message='Неверный инвайт-код')
