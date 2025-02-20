from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, ReservationViewSet, RentalRecordViewSet

# DRF 라우터 생성
router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'rentals', RentalRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
