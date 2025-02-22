import requests
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import ItemService

class ItemView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="물품 리스트 조회"
        , description="전체 물품 리스트를 조회합니다."
        , responses={200: "Reservation List", 400: "400 Error"}
    )
    def post(self, request: Request) -> Response:
        if not request.data['user_id']:
            return Response({"error": "user_id가 필요합니다."}, status=400)

        return Response(ItemService.get_item_list(request.data['user_id']), status=200)

class ItemDetailView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="물품 상세 조회"
        , description="특정 물품에 대한 상세 정보를 조회합니다."
        , responses={200: "Reservation List", 400: "400 Error"}
    )
    def post(self, request: Request) -> Response:
        if not request.data['user_id']:
            return Response({"error": "user_id가 필요합니다."}, status=400)

        return Response(ItemService.get_item_detail(request.data['user_id']), status=200)


class ItemReservationsView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="물품 예약"
        , description="물품을 예약 합니다."
        , responses={200: "Reservation List", 400: "400 Error"}
    )
    def post(self, request: Request) -> Response:
        if not request.data['user_id']:
            return Response({"error": "user_id가 필요합니다."}, status=400)

        return Response(ItemService.item_reservations(request.data['user_id']), status=200)

class ItemReservationsListView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="사용자 물품 조회"
        , description="사용자가 예약한 물품을 조회합니다."
        , responses={200: "Reservation List", 400: "400 Error"}
    )
    def post(self, request: Request) -> Response:
        if not request.data['user_id']:
            return Response({"error": "user_id가 필요합니다."}, status=400)

        return Response(ItemService.get_item_reservations_list(request.data['user_id']), status=200)
    
class ItemPickupView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="물품 픽업"
        , description="사용자가 예약한 물품을 픽업합니다."
        , responses={200: "Reservation List", 400: "400 Error"}
    )
    def post(self, request: Request) -> Response:
        if not request.data['user_id']:
            return Response({"error": "user_id가 필요합니다."}, status=400)

        return Response(ItemService.item_pickup(request.data['user_id']), status=200)
    
class ItemReturnView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="물품 반납"
        , description="사용자가 대여한 물품을 반납합니다."
        , responses={200: "Reservation List", 400: "400 Error"}
    )
    def post(self, request: Request) -> Response:
        if not request.data['user_id']:
            return Response({"error": "user_id가 필요합니다."}, status=400)

        return Response(ItemService.item_return(request.data['user_id']), status=200)

class ItemReturnListView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="물품 반납 조회"
        , description="사용자가 반납한 물품을 조회합니다."
        , responses={200: "Reservation List", 400: "400 Error"}
    )
    def post(self, request: Request) -> Response:
        if not request.data['user_id']:
            return Response({"error": "user_id가 필요합니다."}, status=400)

        return Response(ItemService.get_item_return_list(request.data['user_id']), status=200)