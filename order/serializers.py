from collections import UserDict
from users.serializers import UserInfoSerializer
from .models import Order
from users.models import User
from django.contrib.auth import authenticate
from django.utils import timezone

from rest_framework import serializers

class OrderSerializer(serializers.ModelSerializer):
    user_id = UserInfoSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ('__all__')

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("title","isbn","author","publisher","reason")