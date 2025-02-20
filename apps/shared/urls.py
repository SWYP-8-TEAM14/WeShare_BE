from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ItemViewSet, RentalRecordViewSet, ReservationViewSet

# DRF 라우터 생성
router = DefaultRouter()
router.register(r"items", ItemViewSet)
router.register(r"reservations", ReservationViewSet)
router.register(r"rentals", RentalRecordViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
