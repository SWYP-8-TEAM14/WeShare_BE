from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Item, RentalRecord, Reservation
from .serializers import ItemSerializer, RentalRecordSerializer, ReservationSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    @action(detail=True, methods=["post"])
    def reserve(self, request, pk=None):
        """물품 예약 API"""
        item = self.get_object()
        user_id = request.data.get("user_id")
        start_time = request.data.get("start_time")
        end_time = request.data.get("end_time")

        reservation = Reservation.objects.create(user_id=user_id, item=item, book_date=start_time, status="예약 완료")
        return Response(ReservationSerializer(reservation).data)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    @action(detail=False, methods=["post"])
    def user_reservations(self, request):
        """사용자의 예약 목록 조회"""
        user_id = request.data.get("user_id")
        reservations = Reservation.objects.filter(user_id=user_id)
        return Response(ReservationSerializer(reservations, many=True).data)


class RentalRecordViewSet(viewsets.ModelViewSet):
    queryset = RentalRecord.objects.all()
    serializer_class = RentalRecordSerializer

    @action(detail=True, methods=["post"])
    def pickup(self, request, pk=None):
        """픽업 인증 API"""
        rental = self.get_object()
        rental.rental_status = "대여 중"
        rental.save()
        return Response(RentalRecordSerializer(rental).data)

    @action(detail=True, methods=["post"])
    def return_item(self, request, pk=None):
        """반납 인증 API"""
        rental = self.get_object()
        rental.rental_status = "반납 완료"
        rental.actual_return = request.data.get("return_time")
        rental.save()
        return Response(RentalRecordSerializer(rental).data)
