from .models import Book, Rental

from rest_framework import serializers

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id","title","isbn","author","publisher","book_status")

class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id","title","isbn","author","publisher")

class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ("id","user_id","book_id","rental_date","return_date","is_extension","extension_date")

class RentalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ("user_id","book_id")