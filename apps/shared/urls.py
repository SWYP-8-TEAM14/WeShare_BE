from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemView, ReservationView, RentalRecordView

# DRF 라우터 생성
router = DefaultRouter()
router.register(r'items', ItemView)
router.register(r'reservations', ReservationView)
router.register(r'rentals', RentalRecordView)

urlpatterns = [
    path('', include(router.urls)),
]
