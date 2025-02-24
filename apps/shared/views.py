import requests
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import ItemService

# /api/v1/shared/users
class UserAddView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="신규 인원 추가 테스트"
        , description="신규 인원 추가 테스트"
        , responses={200: "Success", 400: "400 Error"}
    )
    def post(self, request: Request) -> Response:
        item_data = ItemService.put_item(request.data)
        return Response(item_data, status=200 if "errors" not in item_data else 400)

# /api/v1/shared/items
class ItemAddView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="물품 등록"
        , description="신규 물품을 등록합니다."
        , responses={200: "Success", 400: "400 Error"}
    )
    def post(self, request: Request) -> Response:
        if not request.data:
            return Response({"error": "request.data가 필요합니다."}, status=400)
        
        if not request.data['user']:
            return Response({"error": "user 필요합니다."}, status=400)
        
        if not request.data['group_id']:
            return Response({"error": "group_id가 필요합니다."}, status=400)
        
        if not request.data['item_name']:
            return Response({"error": "item_name가 필요합니다."}, status=400)
        
        if not request.data['item_description']:
            return Response({"error": "item_description가 필요합니다."}, status=400)
        
        if not request.data['item_image']:
            return Response({"error": "item_image가 필요합니다."}, status=400)
        
        if not request.data['status']:
            if request.data['status'] != 0:
                return Response({"error": "status가 필요합니다."}, status=400)
        
        if not request.data['quantity']:
            return Response({"error": "quantity가 필요합니다."}, status=400)
        
        if not request.data['caution']:
            return Response({"error": "caution가 필요합니다."}, status=400)
        
        if not request.data['created_at']:
            return Response({"error": "created_at가 필요합니다."}, status=400)
        
        if not request.data['deleted_at']:
            return Response({"error": "deleted_at가 필요합니다."}, status=400)

        item_data = ItemService.put_item(request.data)
        return Response(item_data, status=200 if "errors" not in item_data else 400)



# /api/v1/shared/items
class ItemView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="물품 리스트 조회"
        , description="전체 물품 리스트를 조회합니다."
        , responses={200: "Success", 400: "400 Error"}
    )
    def post(self, request: Request) -> Response:
        if not request.data:
            return Response({"error": "request.data가 필요합니다."}, status=400)
        
        if not request.data['user_id']:
            return Response({"error": "user_id가 필요합니다."}, status=400)

        return Response(ItemService.get_item_list(request.data), status=200)




# /api/v1/shared/items/detail
class ItemDetailView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="물품 상세 조회"
        , description="특정 물품에 대한 상세 정보를 조회합니다."
        , responses={200: "Success", 400: "400 Error"}
    )
    def post(self, request: Request) -> Response:
        if not request.data:
            return Response({"error": "request.data가 필요합니다."}, status=400)
        
        if not request.data['user_id']:
            return Response({"error": "user_id가 필요합니다."}, status=400)
        
        if not request.data['item_id']:
            return Response({"error": "item_id가 필요합니다."}, status=400)


        return Response(ItemService.get_item_detail(request.data), status=200)





# /api/v1/shared/items/reservations
class ItemReservationsView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="물품 예약"
        , description="물품을 예약 합니다."
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
