from gc import get_objects
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from order.permissions import CustomReadOnly
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from django.utils import timezone
from rest_framework.response import Response
from .models import Book, Rental, Reserve
from .serializers import BookSerializer, BookCreateSerializer, RentalCreateSerializer, RentalSerializer, ReserveCreateSerializer, ReserveSerializer

from datetime import datetime
from django.utils.dateformat import DateFormat

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [CustomReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'list' or 'retrieve':
            return BookSerializer
        return BookCreateSerializer

    def perform_create(self, serializer):
        code = 'BK'
        date = DateFormat(datetime.now()).format('Ymd')
        idx = str(Book.objects.filter(id__contains=date).count()+1).zfill(3)
        id = code+date+idx
        serializer.save(id=id)

class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    permission_classes = [CustomReadOnly]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user_id']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return RentalSerializer
        return RentalCreateSerializer

    def perform_create(self, serializer):
        book_id = serializer.validated_data['book_id'].id
        user_id = serializer.validated_data['user_id']
        book = get_object_or_404(Book, pk = book_id)
        book.book_status = 1
        book.save()
        reserve = Reserve.objects.filter(book_id = book_id, reserve_status = 2, user_id = user_id)
        print(user_id)
        if(reserve.exists()):
            reserve_first = reserve.first()
            reserve_first.reserve_status = 3
            reserve_first.save()
        serializer.save()

class ReserveViewSet(viewsets.ModelViewSet):
    queryset = Reserve.objects.all()
    permission_classes = [CustomReadOnly]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user_id']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ReserveSerializer
        return ReserveCreateSerializer

    def perform_create(self, serializer):
        serializer.save()

@api_view(['GET'])
def rent_extension(request,pk):
    rental = get_object_or_404(Rental, pk=pk)
    rental.is_extension = True
    rental.save()
    return Response({'status':'ok'})

@api_view(['GET'])
def book_return(request,pk):
    book = get_object_or_404(Book, pk=pk)
    book.book_status = 2
    book.save()
    return Response({'status':'ok'})

@api_view(['GET'])
def book_complete(request,pk):
    rental = get_object_or_404(Rental, pk=pk)
    rental.return_date = timezone.now()
    rental.save()
    book = get_object_or_404(Book, pk=rental.book_id.id)
    reserve = Reserve.objects.filter(book_id = rental.book_id.id, reserve_status = 0)
    if(reserve.exists()):
        book.book_status = 3
        reserve_first = reserve.first()
        reserve_first.available_date = timezone.now()
        reserve_first.reserve_status = 2
        reserve_first.save()
    else:
        book.book_status = 0
    book.save()
   
    return Response({'status':'ok'})

@api_view(['GET'])
def reserve_cancel(request,pk):
    reserve = get_object_or_404(Reserve, pk=pk)
    reserve.reserve_status = 1
    reserve.save()
    return Response({'status':'ok'})
