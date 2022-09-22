from django.urls import path
from rest_framework import routers
from .views import BookViewSet, RentalViewSet, ReserveViewSet, book_complete, del_reserve, rent_extension, book_return

router = routers.SimpleRouter()
router.register('book',BookViewSet)
router.register('rental',RentalViewSet)
router.register('reserve',ReserveViewSet)

urlpatterns = router.urls+[
    path('extension/<int:pk>/',rent_extension, name='rent_extension'),
    path('return/<str:pk>/',book_return, name='book_return'), 
    path('complete/<int:pk>/',book_complete, name='book_complete'),
    path('del_reserve/<int:pk>/',del_reserve, name='del_reserve'),
]