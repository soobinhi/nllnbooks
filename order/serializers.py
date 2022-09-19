from .models import Order
from django.contrib.auth import authenticate
from django.utils import timezone

from rest_framework import serializers

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id","title","isbn","author","publisher","user_id","reason","order_date","order_status")

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("title","isbn","author","publisher","reason")