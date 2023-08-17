from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import UserProfile
from .serializers import UserProfileSerializer


class UserProfileAPI(APIView):
    def get(self, request):
        phone_number = request.session.get('phone_number')
        try:
            user = UserProfile.objects.get(phone_number=phone_number)
            serializer = UserProfileSerializer(user)
            return Response({'user': serializer.data})
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class ReferralListAPI(APIView):
    def get(self, request):
        user = UserProfile.objects.get(phone_number=request.session['phone_number'])
        referred_users = user.referred_users.all()
        referred_phone_numbers = [user.phone_number for user in referred_users]
        return Response({'referred_users': referred_phone_numbers})