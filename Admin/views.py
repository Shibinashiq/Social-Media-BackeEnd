from rest_framework.views import APIView
from .serializers import UserBlockSerializer
from Auth.models import CustomUser
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny 
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Exclude superusers from the queryset
        return CustomUser.objects.exclude(is_superuser=True)


class UserBlockAPIView(APIView):
    def post(self, request, user_id):
        try:
            user = CustomUser.objects.get(pk=user_id)
            user.blocked = True
            user.save()
            serializer = UserBlockSerializer(user)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class UserUnblockAPIView(APIView):
    def post(self, request, user_id):
        try:
            user = CustomUser.objects.get(pk=user_id)
            user.blocked = False
            user.save()
            serializer = UserBlockSerializer(user)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)