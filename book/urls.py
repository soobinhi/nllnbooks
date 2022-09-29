from django.urls import path
from rest_framework import routers
from .views import BookViewSet, RentalViewSet, ReserveViewSet, book_complete, book_detail, check_overdue, pay_overdue, rent_extension, book_return, rent_submit, reserve_cancel, return_submit

router = routers.SimpleRouter()
router.register('book',BookViewSet)
router.register('rental',RentalViewSet)
router.register('reserve',ReserveViewSet)

urlpatterns = router.urls+[
    path('extension/<int:pk>/',rent_extension, name='rent_extension'),
    path('return/<str:pk>/',book_return, name='book_return'), 
    path('complete/<int:pk>/',book_complete, name='book_complete'),
    path('reserve_cancel/<int:pk>/',reserve_cancel, name='del_reserve'),
    path('detail/<str:pk>/',book_detail, name='book_detail'), 
    path('adminrental/',rent_submit, name='rent_submit'),
    path('adminreturn/',return_submit, name='return_submit'),
    path('check_overdue/<str:user_id>/',check_overdue, name='check_overdue'),
    path('pay_overdue/<str:user_id>/',pay_overdue, name='pay_overdue'),
]