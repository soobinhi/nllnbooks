from django.shortcuts import render

from nllnbooks.settings import REST_FRAMEWORK
from .models import User
from rest_framework import generics, status
from .serializers import LoginSerializer, RegisterSerializer
from rest_framework.response import Response

from users import serializers

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data
        user_id = request.data.get('user_id')
        is_admin = User.objects.get(user_id=user_id).is_admin
        return Response({"token":token.key, "user_id":user_id, "is_admin":is_admin}, status=status.HTTP_200_OK)