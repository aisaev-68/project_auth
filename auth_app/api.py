from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import UserProfile
from .serializers import UserProfileSerializer


class UserProfileAPI(APIView):
    """
    Получение профиля пользователя.

    GET метод:
        Получает номер телефона из сессии, ищет профиль пользователя по номеру
        телефона и сериализует его данные с использованием UserProfileSerializer.
        Возвращает данные профиля пользователя в виде JSON-ответа.
        Если профиль пользователя не найден, возвращает ошибку 404.

    Параметры запроса:
        Отсутствуют.

    Возвращаемые значения:
        Если профиль пользователя найден, возвращает JSON-ответ с данными
        профиля пользователя.
        Если профиль пользователя не найден, возвращает JSON-ответ с ошибкой 404.
    """

    def get(self, request):
        phone_number = request.session.get('phone_number')
        try:
            user = UserProfile.objects.get(phone_number=phone_number)
            serializer = UserProfileSerializer(user)
            return Response({'user': serializer.data})
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class ReferralListAPI(APIView):
    """
    Получение списка приглашенных пользователей.

    GET метод:
        Получает номер телефона из сессии, находит профиль пользователя по
        номеру телефона и извлекает список приглашенных пользователей.
        Сериализует список номеров телефонов приглашенных пользователей и
        возвращает его в виде JSON-ответа.

    Параметры запроса:
        Отсутствуют.

    Возвращаемые значения:
        Возвращает JSON-ответ с списком номеров телефонов приглашенных пользователей.
    """

    def get(self, request):
        user = UserProfile.objects.get(phone_number=request.session['phone_number'])
        referred_users = user.referred_users.all()
        referred_phone_numbers = [user.phone_number for user in referred_users]
        return Response({'referred_users': referred_phone_numbers})
