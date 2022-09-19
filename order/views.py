from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from order.permissions import CustomReadOnly

from datetime import datetime
from django.utils.dateformat import DateFormat

from users.models import User
from book.models import Book
from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [CustomReadOnly]
    
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
    print(order.order_status)
    if(order.order_status == 3):
        print('입고완료')
        code='BK'
        date = DateFormat(datetime.now()).format('Ymd')
        idx = str(Book.objects.filter(id__contains=date).count()+1).zfill(3)
        Book.objects.create(
            id = code+date+idx,
            title = order.title,
            isbn = order.isbn,
            author = order.author,
            publisher = order.publisher
        )
    return Response({'status':'ok'})

