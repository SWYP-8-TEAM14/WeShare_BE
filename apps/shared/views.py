import json
import requests
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
# from .services import ItemService
from .serializers import (
    ItemAddSerializer,
    ItemListSerializer,
    ItemDetailSerializer,
    ItemReservationsSerializer,
    ItemReservationsListSerializer,
    ItemPickupSerializer,
    ItemReturnSerializer,
    ItemReturnListSerializer,
)

# /api/v1/shared/items
class ItemAddView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="물품 등록"
        , description="신규 물품을 등록합니다."
        , request=ItemAddSerializer
        , responses={200: "Success", 400: "400 Error"}
    )
    def post(self, request: Request) -> Response:
        serializer = ItemAddSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "Result": 0,
                    "Message": serializer.errors,
                    "data": ""
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # DB 저장
        item = serializer.save()
        # 저장 후, 간단한 정보만 내려줄 수도 있고, 전체 정보를 내려줄 수도 있음
        created_data = {
            "item_id": item.item_id,
            "item_name": item.item_name
        }
        return Response(
            {
                "Result": 1,
                "Message": "",
                "data": json.dumps(created_data, default=str)
            },
            status=status.HTTP_201_CREATED
        )



# /api/v1/shared/items
class ItemView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="물품 리스트 조회"
        , description="전체 물품 리스트를 조회합니다."
        , request=ItemListSerializer
        , responses={200: "Success", 400: "400 Error"}
    )
    def post(self, request):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response(
                {
                    "Result": 0,
                    "Message": "user_id는 필수입니다.",
                    "data": ""
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        items = Item.objects.filter(user_id=user_id).order_by("-created_at")
        serializer = ItemListSerializer(items, many=True)
        # serializer.data는 이미 list[dict] 형태
        return Response(
            {
                "Result": 1,
                "Message": "",
                "data": json.dumps(serializer.data, default=str)
            },
            status=status.HTTP_200_OK
        )




# /api/v1/shared/items/detail
class ItemDetailView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="물품 상세 조회"
        , description="특정 물품에 대한 상세 정보를 조회합니다."
        , request=ItemDetailSerializer
        , responses={200: "Success", 400: "400 Error"}
    )
    def post(self, request):
        user_id = request.data.get("user_id")
        item_id = request.data.get("item_id")

        if not user_id:
            return Response(
                {
                    "Result": 0,
                    "Message": "user_id는 필수입니다.",
                    "data": ""
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if not item_id:
            return Response(
                {
                    "Result": 0,
                    "Message": "item_id는 필수입니다.",
                    "data": ""
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            item = Item.objects.get(user_id=user_id, item_id=item_id)
        except Item.DoesNotExist:
            return Response(
                {
                    "Result": 0,
                    "Message": "해당 아이템이 존재하지 않거나 user_id가 일치하지 않습니다.",
                    "data": ""
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ItemDetailSerializer(item)
        return Response(
            {
                "Result": 1,
                "Message": "",
                "data": json.dumps(serializer.data, default=str)
            },
            status=status.HTTP_200_OK
        )





# /api/v1/shared/items/reservations
class ItemReservationsView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="물품 예약"
        , description="물품을 예약 합니다."
        , request=ItemReservationsSerializer
        , responses={200: "Success", 400: "400 Error"}
    )
    def post(self, request: Request) -> Response:
        if not request.data:
            return Response({"error": "request.data가 필요합니다."}, status=400)
        
        if not request.data['user_id']:
            return Response({"error": "user_id가 필요합니다."}, status=400)
        
        if not request.data['item_id']:
            return Response({"error": "item_id가 필요합니다."}, status=400)
        
        if not request.data['start_time']:
            return Response({"error": "start_time이 필요합니다."}, status=400)
        
        if not request.data['end_time']:
            return Response({"error": "end_time이 필요합니다."}, status=400)

        return Response(ItemService.item_reservations(request.data), status=200)




# /api/v1/shared/items/reservations/list
class ItemReservationsListView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="사용자 물품 조회"
        , description="사용자가 예약한 물품을 조회합니다."
        , request=ItemReservationsListSerializer
        , responses={200: "Success", 400: "400 Error"}
    )
    def post(self, request: Request) -> Response:
        # if not request.data['user_id']:
        #     return Response({"error": "user_id가 필요합니다."}, status=400)

        return Response(ItemService.get_item_reservations_list(request.data), status=200)
    
    
    
    
# /api/v1/shared/items/pickup
class ItemPickupView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="물품 픽업"
        , description="사용자가 예약한 물품을 픽업합니다."
        , request=ItemPickupSerializer
        , responses={200: "Success", 400: "400 Error"}
    )
    def post(self, request: Request) -> Response:
        if not request.data:
            return Response({"error": "request.data가 필요합니다."}, status=400)
        
        if not request.data['user_id']:
            return Response({"error": "user_id가 필요합니다."}, status=400)
        
        if not request.data['item_id']:
            return Response({"error": "item_id가 필요합니다."}, status=400)
        
        if not request.data['pickup_time']:
            return Response({"error": "pickup_time이 필요합니다."}, status=400)
        
        if not request.data['image']:
            return Response({"error": "image가 필요합니다."}, status=400)

        return Response(ItemService.item_pickup(request.data), status=200)




# /api/v1/shared/items/return/list
class ItemReturnView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="물품 반납"
        , description="사용자가 대여한 물품을 반납합니다."
        , request=ItemReturnSerializer
        , responses={200: "Success", 400: "400 Error"}
    )
    def post(self, request: Request) -> Response:
        if not request.data:
            return Response({"error": "request.data가 필요합니다."}, status=400)
        
        if not request.data['user_id']:
            return Response({"error": "user_id가 필요합니다."}, status=400)

        return Response(ItemService.item_return(request.data), status=200)




    # /api/v1/shared/items/return
class ItemReturnListView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="물품 반납 조회"
        , description="사용자가 반납한 물품을 조회합니다."
        , request=ItemReturnListSerializer
        , responses={200: "Success", 400: "400 Error"}
    )
    def post(self, request: Request) -> Response:
        if not request.data:
            return Response({"error": "request.data가 필요합니다."}, status=400)
        
        if not request.data['user_id']:
            return Response({"error": "user_id가 필요합니다."}, status=400)
        
        if not request.data['item_id']:
            return Response({"error": "item_id가 필요합니다."}, status=400)
        
        if not request.data['return_time']:
            return Response({"error": "return_time이 필요합니다."}, status=400)
        
        if not request.data['return_image']:
            return Response({"error": "return_image이 필요합니다."}, status=400)

        return Response(ItemService.get_item_return_list(request.data), status=200)
