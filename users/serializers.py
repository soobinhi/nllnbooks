from .models import User, Userlog
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.utils import timezone

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

class RegisterSerializer(serializers.ModelSerializer):
    
    user_id = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            user_id = validated_data['user_id'],
            name = validated_data['name'],
            password = validated_data['password']
        )
        token = Token.objects.create(user=user)
        return user
    class Meta:
        model = User
        fields = ['user_id', 'email', 'name', 'password']

class LoginSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user=user)
            log = Userlog.objects.create(
                user_id = user,
                login_date = timezone.now()
            )
            return token
        raise serializers.ValidationError(
            {"error": "Unable to log in with provided credentials."}
        )

