from time import timezone
from tkinter import CASCADE
from django.db import models
from users.models import User
from django.utils import timezone
from datetime import datetime, timedelta

class Book(models.Model):
    id = models.CharField(primary_key=True, max_length=20, unique=True)
    title = models.CharField(max_length=150)
    isbn = models.CharField(max_length=20)
    author = models.CharField(max_length=150)
    publisher = models.CharField(max_length=150)
    book_status = models.IntegerField(default=0)
    # status 0 : 대여 가능 / 1: 대여중 / 2: 반납승인대기 / 3: 예약대기 
    
class Rental(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_rental')
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_rental')
    rental_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(null=True)
    is_extension = models.BooleanField(default=False)
    
class Reserve(models.Model): 
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reserve')
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_reserve')
    reserve_date = models.DateTimeField(default=timezone.now)
    available_date = models.DateTimeField(null=True)
    reserve_status = models.IntegerField(default=0)
    # status 0 : 예약 / 1: 예약취소 / 2: 대여가능 / 3: 대여완료
    
class overdue(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_overdue')
    overdue_period = models.IntegerField(null=False)
    pay_dated = models.DateTimeField(default=timezone.now)

