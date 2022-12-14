from time import timezone
from django.db import models
from users.models import User
from django.utils import timezone

class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    isbn = models.CharField(max_length=20)
    author = models.CharField(max_length=150)
    publisher = models.CharField(max_length=150)
    reason = models.TextField(null=True)
    order_status = models.IntegerField(default=1)
    order_date = models.DateTimeField(default=timezone.now)
    image = models.TextField(default='https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg')
    
    