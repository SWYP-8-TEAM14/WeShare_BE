import requests
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Item, Reservation, RentalRecord
from .serializers import ItemSerializer, ReservationSerializer, RentalRecordSerializer

class ItemView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        summary="물품 리스트 조회"
        , description="전체 물품 리스트를 반환합니다."
        , responses=ItemSerializer
    )

    def post(self, request: Request) -> Response:
        serializer = ItemSerializer(data=request.data)

        return Response()

class ReservationView(APIView):
    permission_classes = [IsAuthenticated]


class RentalRecordView(APIView):
    permission_classes = [IsAuthenticated]
