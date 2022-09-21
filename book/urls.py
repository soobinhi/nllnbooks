from django.urls import path
from rest_framework import routers
from .views import BookViewSet, RentalViewSet, book_complete, rent_extension, book_return

router = routers.SimpleRouter()
router.register('book',BookViewSet)
router.register('rental',RentalViewSet)

urlpatterns = router.urls+[
    path('extension/<int:pk>/',rent_extension, name='rent_extension'),
    path('return/<str:pk>/',book_return, name='book_return'), 
    path('complete/<int:pk>/',book_complete, name='book_complete'),
]