from email.mime import image
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from order.permissions import CustomReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.utils import timezone

from users.models import User
from book.models import Book, Reserve
from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [CustomReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user_id']
    def get_serializer_class(self):
        if self.action == 'list' or 'retrieve':
            return OrderSerializer
        return OrderCreateSerializer

    def perform_create(self, serializer):
        user = User.objects.get(user_id=self.request.user)
        serializer.save(user_id=user)

@api_view(['GET'])
def change_status(request,pk):
    order = get_object_or_404(Order, pk=pk)
    order.order_status += 1 
    order.save()
    if(order.order_status == 3):
        code='BK'
        date = DateFormat(datetime.now()).format('Ymd')
        idx = str(Book.objects.filter(id__contains=date).count()+1).zfill(3)
        book_id = code+date+idx
        Book.objects.create(
            id = book_id,
            title = order.title,
            isbn = order.isbn,
            author = order.author,
            publisher = order.publisher,
            image = order.image,
            book_status = 3
        )
        book = get_object_or_404(Book,pk=book_id)
        Reserve.objects.create(
            user_id = order.user_id,
            book_id = book
        )
    return Response({'status':'ok'})

@api_view(['GET'])
def order_check(request,user_id):
    now = timezone.now().date()
    order = Order.objects.filter(user_id=user_id)
    order_last = order.last()
    order_date = order_last.order_date.date()
    diff = now-order_date
    if(diff.days<30):
        return Response({'status':'fail'})
    return Response({'status':'ok'})