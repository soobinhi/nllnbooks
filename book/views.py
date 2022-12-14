
from asyncio.windows_events import NULL
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from order.permissions import CustomReadOnly
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework.response import Response

from users.models import User
from .models import Book, Overdue, Rental, Reserve, ReserveAlarmLog, Overdue
from .serializers import BookSerializer, BookCreateSerializer, RentalCreateSerializer, RentalSerializer, ReserveCreateSerializer, ReserveSerializer


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
    filterset_fields = ['user_id','book_id']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return RentalSerializer
        return RentalCreateSerializer()

    def perform_create(self, serializer):
        book_id = serializer.validated_data['book_id'].id
        user_id = serializer.validated_data['user_id']
        book = get_object_or_404(Book, pk = book_id)
        book.book_status = 1
        book.save()
        reserve = Reserve.objects.filter(book_id = book_id, reserve_status = 2, user_id = user_id)
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book_id = serializer.validated_data['book_id'].id
        user_id = serializer.validated_data['user_id']
        reserve = Reserve.objects.filter(book_id = book_id, user_id = user_id, reserve_status__in=[0,2])
        if(reserve.exists()):
            return Response({'status':'fail'})
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
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

@api_view(['GET'])
def book_detail(request,pk):
    book = get_object_or_404(Book, pk=pk)
    serializer = BookSerializer(book)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def rent_submit(request):
    data = request.data.copy()
    for item in data:
        serializer = RentalCreateSerializer(data=item)
        if serializer.is_valid():
            book_id = item['book_id']
            user_id = item['user_id']
            book = get_object_or_404(Book, pk = book_id)
            book.book_status = 1
            book.save()
            reserve = Reserve.objects.filter(book_id = book_id, reserve_status = 2, user_id = user_id)
            if(reserve.exists()):
                reserve_first = reserve.first()
                reserve_first.reserve_status = 3
                reserve_first.save()
            serializer.save()
    return Response({'status':'ok'})

@api_view(['POST'])
def return_submit(request):
    data = request.data.copy()
    for item in data:
        #Rental ???????????? Return ?????? ?????? 
        rental = get_object_or_404(Rental, pk=item['id'])
        rental.return_date = timezone.now()
        rental.save()
        #????????? ??? ????????? ?????? ???????????? 
        book = get_object_or_404(Book, pk=rental.book_id.id)
        #?????? ?????? ?????? ?????? ????????? ?????? 
        reserve = Reserve.objects.filter(book_id = book.id, reserve_status = 0)
        if(reserve.exists()):
            #?????? ?????? ?????? ????????? ?????? ??????
            book.book_status = 3
            reserve_first = reserve.first()
            reserve_first.available_date = timezone.now()
            reserve_first.reserve_status = 2
            reserve_first.save()
            user = get_object_or_404(User, pk=reserve_first.user_id)
            #??????????????? ?????? ?????? ?????? ??????
            alarmlog = ReserveAlarmLog()
            alarmlog.user_id = reserve_first.user_id
            alarmlog.book_id = book.id
            alarmlog.email = user.email
            alarmlog.save()
        else:
            book.book_status = 0
        book.save()
        #??????????????? ??????
        schedueled_date = rental.rental_date
        schedueled_date = schedueled_date + timedelta(days=21)
        #???????????? ?????? ??????????????? +7???
        if(rental.is_extension):
            schedueled_date = schedueled_date + timedelta(days=7)
        now = timezone.now().date()
        diff = now - schedueled_date.date()
        #??????????????? ??????????????? ????????????????????? ?????? ?????? ????????? ?????? ?????? ????????? ?????? 
        if(diff.days>0):
            overdue = Overdue()
            overdue.overdue_period = diff.days
            overdue.rental_id = rental
            overdue.save()
    return Response({'status':'ok'})

@api_view(['GET'])
def check_overdue(request,user_id):
    overdue_rental = Rental.objects.filter(return_date__isnull = True, user_id=user_id)
    now = timezone.now().date()
    for item in overdue_rental:
        schedueled_date = item.rental_date
        schedueled_date = schedueled_date + timedelta(days=21)
        #???????????? ?????? ??????????????? +7???
        if(item.is_extension):
            schedueled_date = schedueled_date + timedelta(days=7)
        diff = now - schedueled_date.date()
        #???????????? ??? ?????? ????????? ??? ?????? return
        if(diff.days>0):
            return Response({'status':'fail'})
    #?????? ????????? ???????????? ????????? ???????????? ???????????? ?????? ????????? ????????????
    rentlist = Rental.objects.filter(user_id=user_id, return_date__isnull = False).values('id')
    overdue = Overdue.objects.filter(rental_id__in = rentlist, pay_date__isnull = True)
    data = 0
    #???????????? - ???????????? ?????? ??????????????? ??? ????????? ??? ????????? ????????? ????????? ????????? 
    for item in overdue:
        ovdedue_date = item.overdue_date.date()
        diff = now - ovdedue_date
        if(item.overdue_period>diff.days):
            data = data+item.overdue_period - diff.days
    return Response({'status':'ok', 'data':data})

@api_view(['GET'])
def pay_overdue(request,user_id):
    now = timezone.now().date()
    #?????? ????????? ???????????? ????????? ???????????? ???????????? ?????? ????????? ????????????
    rentlist = Rental.objects.filter(user_id=user_id, return_date__isnull = False).values('id')
    overdue = Overdue.objects.filter(rental_id__in = rentlist, pay_date__isnull = True)
    data = 0
    #????????? ???????????? ???????????? ????????? pay_date ??????
    for item in overdue:
        ovdedue_date = item.overdue_date.date()
        diff = now - ovdedue_date
        if(item.overdue_period>diff.days):
            item.pay_date = timezone.now()
            item.save()
    return Response({'status':'ok', 'data':data})