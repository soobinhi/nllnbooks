from rest_framework import routers
from .views import BookViewSet, RentalViewSet

router = routers.SimpleRouter()
router.register('book',BookViewSet)
router.register('rental',RentalViewSet)

urlpatterns = router.urls