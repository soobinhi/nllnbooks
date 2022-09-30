from django.urls import path
from rest_framework import routers
from .views import OrderViewSet, change_status, order_check

router = routers.SimpleRouter()
router.register('',OrderViewSet)

urlpatterns = router.urls +[
    path('status/<int:pk>/',change_status, name='change_status'),
    path('check/<str:user_id>/',order_check, name='order_check'),
]