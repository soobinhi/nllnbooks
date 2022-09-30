from users.serializers import UserInfoSerializer
from .models import Book, Rental, Reserve
from rest_framework import serializers

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id","title","isbn","author","publisher","book_status","image")

class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id","title","isbn","author","publisher","image")

class RentalSerializer(serializers.ModelSerializer):
    user_id = UserInfoSerializer(read_only=True)
    book_id = BookSerializer(read_only=True)
    overdue_data = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Rental
        fields = ("id","user_id","overdue_data","book_id","rental_date","return_date","is_extension")

class RentalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ("user_id","book_id","rental_date")

class ReserveSerializer(serializers.ModelSerializer):
    user_id = UserInfoSerializer(read_only=True)
    book_id = BookSerializer(read_only=True)
    class Meta:
        model = Reserve
        fields = ('__all__')

class ReserveCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserve
        fields = ("user_id","book_id")