from django.urls import path
from rest_framework import routers
from .views import BookViewSet, RentalViewSet, ReserveViewSet, book_complete, rent_extension, book_return, reserve_cancel

router = routers.SimpleRouter()
router.register('book',BookViewSet)
router.register('rental',RentalViewSet)
router.register('reserve',ReserveViewSet)

urlpatterns = router.urls+[
    path('extension/<int:pk>/',rent_extension, name='rent_extension'),
    path('return/<str:pk>/',book_return, name='book_return'), 
    path('complete/<int:pk>/',book_complete, name='book_complete'),
    path('reserve_cancel/<int:pk>/',reserve_cancel, name='del_reserve'),
]