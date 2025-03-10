import json
from django.db import connection
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiResponse
from .utils import upload_to_ncp_storage

from .repository import ItemRepository, WishlistRepository
from .serializers import (
    ItemAddSwaggerSerializer,
    ItemListSwaggerSerializer,
    CommonResponseSerializer,
    ItemListRequestSerializer,
    ItemDetailRequestSerializer,
    ItemDeleteRequestSerializer,
    ItemUserListRequestSerializer,
    ItemReserveRequestSerializer,
    WishListToggleRequestSerializer,
    ItemDetailResponseSerializer,
    ItemListResponseSerializer,
    ItemReserveResponseSerializer,
    ItemReserveListResponseSerializer,
    ItemPickupResponseSerializer,
    ItemReturnableListResponseSerializer,
    ItemReturnResponseSerializer,
    WishlistToggleResponseSerializer,
    ItemPickupRequestSerializer,
    ItemAvailableTimeRequestSerializer,
    ItemAvailableTimeResponseSerializer,
    ItemAvailableTimeRangeRequestSerializer,
    ItemAvailableTimeRangeResponseSerializer,
)


class ItemAddView(APIView):
    """
    POST /api/v1/shared/items/add
    """
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = ItemRepository()

    @extend_schema(
        summary="물품 등록",
        description="신규 물품을 등록합니다. images 리스트에 파일 업로드 해주세요(postman 테스트 가능, 스웨그 불가)",
        request=ItemAddSwaggerSerializer,
        responses={
            201: OpenApiResponse(
                response=CommonResponseSerializer,
                description="등록 성공 (Result=1)"
            ),
            400: OpenApiResponse(
                description="등록 실패 (Result=0)"
            )
        },
    )
    def post(self, request):
        data = request.data
        images = request.FILES.getlist("images")

        if not data.get("user_id") and data.get("user_id") != 0:
            return Response({
                "Result": 0,
                "Message": "user_id가 필요합니다.",
                "data": ""
            }, status=400)
        if not data.get("group_id") and data.get("group_id") != 0:
            return Response({
                "Result": 0,
                "Message": "group_id가 필요합니다.",
                "data": ""
            }, status=400)
        if not data.get("item_name"):
            return Response({
                "Result": 0,
                "Message": "item_name이 필요합니다.",
                "data": ""
            }, status=400)

        try:
            new_id = self.repository.create_item(data)

            image_urls = []
            for image in images[:4]:
                image_url = upload_to_ncp_storage(image)
                image_urls.append(image_url)

                self.repository.create_item_image(new_id, image_url)

        except Exception as e:
            return Response({
                "Result": 0,
                "Message": str(e),
                "data": ""
            }, status=400)

        response_data = {
            "item_id": new_id,
            "item_name": data["item_name"]
        }
        return Response({
            "Result": 1,
            "Message": "",
            "data": json.dumps(response_data, default=str)
        }, status=201)

class ItemDeleteView(APIView):
    """
    [POST] /api/v1/shared/items/delete
    """
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = ItemRepository()

    @extend_schema(
        summary="물품 삭제",
        description="등록된 물품을 삭제 (hard delete) 합니다.",
        request=ItemDeleteRequestSerializer,
        responses={
            200: OpenApiResponse(description="삭제 성공/실패 여부 반환"),
            400: OpenApiResponse(description="에러")
        }
    )
    def post(self, request):
        item_ids = request.data.get("item_id")
        if len(item_ids) == 0:
            return Response({"Result":0,"Message":"item_id가 필요합니다.","data":""}, status=400)

        deleted_count = self.repository.delete_item(list(item_ids))
        if deleted_count > 0:
            return Response({"Result":1,"Message":"","data":""}, status=200)
        else:
            return Response({"Result":0,"Message":"해당 item_id가 존재하지 않습니다.","data":""}, status=404)


class ItemView(APIView):
    """
    POST /api/v1/shared/items/
    """
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = ItemRepository()

    @extend_schema(
        summary="물품 리스트 조회",
        description="특정 user_id가 등록한 물품 목록을 조회합니다.",
        request=ItemListRequestSerializer,
        responses={
            200: OpenApiResponse(
                response=ItemListResponseSerializer,
                description="조회 성공 (Result=1)"
            ),
            400: OpenApiResponse(
                description="조회 실패 (Result=0)"
            )
        },
    )
    def post(self, request):
        user_id = request.data.get("user_id")
        group_id = request.data.get("group_id")
        sort = request.data.get("sort")
        is_all = request.data.get("is_all")
        if not user_id and user_id != 0:
            return Response({
                "Result": 0,
                "Message": "user_id가 필요합니다.",
                "data": ""
            }, status=400)
        
        if not group_id and group_id != 0:
            return Response({
                "Result": 0,
                "Message": "group_id가 필요합니다.",
                "data": ""
            }, status=400)
        
        if not sort and sort != 0:
            return Response({
                "Result": 0,
                "Message": "sort (정렬) 값이 없습니다.",
                "data": ""
            }, status=400)
        
        sorted = "DESC"
        if sort == 2:
            sorted = "ASC"
        
        try:
            result_list = self.repository.get_item_list(int(group_id), int(user_id), sorted, is_all)
        except Exception as e:
            return Response({"Result": 0, "Message": str(e), "data": ""}, status=400)

        return Response({
            "Result": 1,
            "Message": "",
            "data": json.dumps(result_list, default=str)
        }, status=200)


class ItemDetailView(APIView):
    """
    POST /api/v1/shared/items/detail/
    """
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = ItemRepository()

    @extend_schema(
        summary="물품 상세 조회",
        description="특정 user_id와 item_id로 1건 상세 정보를 조회합니다.",
        request=ItemDetailRequestSerializer,
        responses={
            200: OpenApiResponse(
                response=ItemDetailResponseSerializer,
                description="조회 성공 (Result=1)"
            ),
            400: OpenApiResponse(
                description="조회 실패 (Result=0)"
            ),
            404: OpenApiResponse(
                description="데이터 없음"
            )
        },
    )
    def post(self, request):
        user_id = request.data.get("user_id")
        item_id = request.data.get("item_id")

        if not user_id and user_id != 0:
            return Response({"Result": 0, "Message": "user_id가 필요합니다.", "data": ""}, status=400)
        if not item_id and item_id != 0:
            return Response({"Result": 0, "Message": "item_id가 필요합니다.", "data": ""}, status=400)

        try:
            detail_data = self.repository.get_item_detail(int(item_id))
        except Exception as e:
            return Response({"Result": 0, "Message": str(e), "data": ""}, status=400)

        if not detail_data:
            return Response({"Result": 0, "Message": "해당 데이터가 존재하지 않습니다.", "data": ""}, status=404)

        return Response({
            "Result": 1,
            "Message": "",
            "data": json.dumps(detail_data, default=str)
        }, status=200)
    

class ItemAvailableTimeView(APIView):
    """
    POST /api/v1/shared/items/available-time/
    """
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = ItemRepository()

    @extend_schema(
        summary="예약 가능한 시간 조회",
        description="특정 item_id에 대한 예약 가능한 시간 범위를 조회합니다.",
        request=ItemAvailableTimeRequestSerializer,
        responses={
            200: OpenApiResponse(response=ItemAvailableTimeResponseSerializer, description="조회 성공 (Result=1)"),
            400: OpenApiResponse(response=CommonResponseSerializer, description="조회 실패 (Result=0)")
        }
    )
    def post(self, request):
        user_id = request.data.get("user_id")
        item_id = request.data.get("item_id")

        if not user_id and user_id != 0:
            return Response({"Result": 0, "Message": "user_id가 필요합니다.", "data": ""}, status=400)
        if not item_id and item_id != 0:
            return Response({"Result": 0, "Message": "item_id가 필요합니다.", "data": ""}, status=400)

        try:
            available_times = self.repository.get_available_times(int(item_id))
        except Exception as e:
            return Response({"Result": 0, "Message": str(e), "data": ""}, status=400)

        return Response({"Result": 1, "Message": "", "data": available_times}, status=200)

class ItemAvailableTimeRangeView(APIView):
    """
    POST /api/v1/shared/items/available-time-range/
    """
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = ItemRepository()

    @extend_schema(
        summary="예약 가능한 시간 범위 조회",
        description="특정 item_id에 대한 예약 가능한 시간 범위를 조회합니다.",
        request=ItemAvailableTimeRangeRequestSerializer,
        responses={
            200: OpenApiResponse(response=ItemAvailableTimeRangeResponseSerializer, description="조회 성공 (Result=1)"),
            400: OpenApiResponse(response=CommonResponseSerializer, description="조회 실패 (Result=0)")
        }
    )
    def post(self, request):
        user_id = request.data.get("user_id")
        item_id = request.data.get("item_id")

        if not user_id and user_id != 0:
            return Response({"Result": 0, "Message": "user_id가 필요합니다.", "data": ""}, status=400)
        if not item_id and item_id != 0:
            return Response({"Result": 0, "Message": "item_id가 필요합니다.", "data": ""}, status=400)

        try:
            available_ranges = self.repository.get_available_time_ranges(int(item_id))
        except Exception as e:
            return Response({"Result": 0, "Message": str(e), "data": ""}, status=400)

        return Response({"Result": 1, "Message": "", "data": available_ranges}, status=200)

class ItemReserveView(APIView):
    """
    [POST] /api/v1/shared/items/reserve
    """
    permission_classes = [AllowAny]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = ItemRepository()

    @extend_schema(
        summary="물품 예약",
        description="물품 예약을 진행합니다. 물품 상태: (기본=0, 예약중=1, 픽업중=2)",
        request=ItemReserveRequestSerializer,
        responses={
            200: OpenApiResponse(response=ItemReserveResponseSerializer, description="예약 성공 (Result=1)"),
            400: OpenApiResponse(description="에러 (Result=0)")
        }
    )
    def post(self, request):
        user_id = request.data.get("user_id")
        item_id = request.data.get("item_id")
        rental_start = request.data.get("rental_start")
        rental_end   = request.data.get("rental_end")

        if not user_id and user_id != 0:
            return Response({"Result":0,"Message":"필수필드(user_id, item_id, rental_start, rental_end) 누락","data":""}, status=400)
        if not item_id and item_id != 0:
            return Response({"Result":0,"Message":"필수필드(user_id, item_id, rental_start, rental_end) 누락","data":""}, status=400)
        if not rental_start or not rental_end:
            return Response({"Result":0,"Message":"필수필드(user_id, item_id, rental_start, rental_end) 누락","data":""}, status=400)

        try:
            self.repository.reserve_item(int(user_id), int(item_id), rental_start, rental_end)
        except Exception as e:
            return Response({"Result":0,"Message":str(e),"data":""}, status=400)

        return Response({"Result":1,"Message":"","data":""}, status=200)
    
class ItemReserveListView(APIView):
    """
    [POST] /api/v1/shared/items/reserve/list
    """
    permission_classes = [AllowAny]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = ItemRepository()

    @extend_schema(
        summary="예약한 물품 조회",
        description="특정 user 가 예약한 물품 목록을 조회합니다.",
        request=ItemUserListRequestSerializer,
        responses={
            200: OpenApiResponse(response=ItemReserveListResponseSerializer, description="조회 성공 (Result=1)"),
            400: OpenApiResponse(description="오류 (Result=0)")
        }
    )
    def post(self, request):
        user_id = request.data.get("user_id")
        group_id = request.data.get("group_id")
        sort = request.data.get("sort")
        if not user_id and user_id != 0:
            return Response({
                "Result": 0,
                "Message": "user_id가 필요합니다.",
                "data": ""
            }, status=400)
        
        if not group_id and group_id != 0:
            return Response({
                "Result": 0,
                "Message": "group_id가 필요합니다.",
                "data": ""
            }, status=400)
        
        if not sort and sort != 0:
            return Response({
                "Result": 0,
                "Message": "sort (정렬) 값이 없습니다.",
                "data": ""
            }, status=400)
        
        sorted = "DESC"
        if sort == 2:
            sorted = "ASC"

        try:
            rows = self.repository.get_reserved_items(int(group_id), int(user_id), sorted)
        except Exception as e:
            return Response({"Result":0,"Message":str(e),"data":""}, status=400)

        return Response({"Result":1,"Message":"","data":str(rows)}, status=200)

class ItemPickupView(APIView):
    """
    [POST] /api/v1/shared/items/pickup
    """
    permission_classes = [AllowAny]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = ItemRepository()

    @extend_schema(
        summary="픽업 인증",
        description="사용자가 예약한 물품을 실제로 픽업합니다.",
        request=ItemPickupRequestSerializer,
        responses={
            200: OpenApiResponse(response=ItemPickupResponseSerializer, description="픽업 성공"),
            400: OpenApiResponse(description="에러"),
            404: OpenApiResponse(description="예약 내역 없음")
        }
    )
    def post(self, request):
        user_id = request.data.get("user_id")
        item_id = request.data.get("item_id")
        pickup_time = request.data.get("pickup_time")

        if not user_id and user_id != 0:
            return Response({"Result":0,"Message":"(user_id, item_id, pickup_time)는 필수입니다.","data":""}, status=400)
        if not item_id and item_id != 0:
            return Response({"Result":0,"Message":"(user_id, item_id, pickup_time)는 필수입니다.","data":""}, status=400)
        if not pickup_time:
            return Response({"Result":0,"Message":"(user_id, item_id, pickup_time)는 필수입니다.","data":""}, status=400)

        try:
            pickup_image = request.FILES.getlist("pickup_image")
            image_urls = []
            for image in pickup_image[:4]:
                image_url = upload_to_ncp_storage(image)
                image_urls.append(image_url)

            result = self.repository.pickup_item(int(user_id), int(item_id), pickup_time, image_urls)
        except Exception as e:
            return Response({"Result":0,"Message":str(e),"data":""}, status=400)

        if not result:
            return Response({"Result":0,"Message":"해당 예약을 찾을 수 없습니다.","data":""}, status=404)

        return Response({
            "Result":1,
            "Message":"",
            "data":str(result)
        }, status=200)

class ItemReturnableListView(APIView):
    """
    [POST] /api/v1/shared/items/return/list
    """
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = ItemRepository()

    @extend_schema(
        summary="반납 가능 물품 조회",
        description="현재 대여중(rental_status='ON_RENT')인 물품 목록 조회",
        request=None,
        responses={
            200: OpenApiResponse(response=ItemReturnableListResponseSerializer, description="조회 성공 (Result=1)"),
            400: OpenApiResponse(description="오류 (Result=0)")
        }
    )
    def post(self, request):
        user_id = request.data.get("user_id")
        if not user_id and user_id != 0:
            return Response({"Result":0,"Message":"user_id가 필요합니다.","data":""}, status=400)

        try:
            rows = self.repository.get_returnable_items(int(user_id))
        except Exception as e:
            return Response({"Result":0,"Message":str(e),"data":""}, status=400)

        return Response({
            "Result":1,
            "Message":"",
            "data":str(rows)
        }, status=200)

class ItemReturnView(APIView):
    """
    [POST] /api/v1/shared/items/return
    """
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = ItemRepository()

    @extend_schema(
        summary="반납 인증",
        description="대여중인 물품을 반납 처리 (rental_records 업데이트)",
        request=None,
        responses={
            200: OpenApiResponse(response=ItemReturnResponseSerializer, description="반납 완료 (Result=1)"),
            400: OpenApiResponse(description="오류 (Result=0)"),
            404: OpenApiResponse(description="반납할 내역 없음")
        }
    )
    def post(self, request):
        user_id = request.data.get("user_id")
        item_id = request.data.get("item_id")
        return_time = request.data.get("return_time")

        if not user_id and user_id != 0:
            return Response({"Result":0,"Message":"필수필드(user_id, item_id, return_time) 누락","data":""}, status=400)
        if not item_id and item_id != 0:
            return Response({"Result":0,"Message":"필수필드(user_id, item_id, return_time) 누락","data":""}, status=400)
        if not return_time:
            return Response({"Result":0,"Message":"필수필드(user_id, item_id, return_time) 누락","data":""}, status=400)

        try:
            return_image = request.FILES.getlist("return_image")
            image_urls = []
            for image in return_image[:4]:
                image_url = upload_to_ncp_storage(image)
                image_urls.append(image_url)
            result = self.repository.return_item(int(user_id), int(item_id), return_time, image_urls)
        except Exception as e:
            return Response({"Result":0,"Message":str(e),"data":""}, status=400)

        if not result:
            return Response({"Result":0,"Message":"대여중인 내역이 없습니다.","data":""}, status=404)

        return Response({
            "Result":1,
            "Message":"",
            "data": str(result)
        }, status=200)


class WishlistToggleView(APIView):
    """
    POST /api/v1/wishlist/
    """
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = WishlistRepository()

    @extend_schema(
        summary="찜 추가/삭제",
        description="찜 추가, 삭제 (1: 추가, 0: 삭제)",
        request=WishListToggleRequestSerializer,
        responses={
            201: OpenApiResponse(
                response=WishlistToggleResponseSerializer,
                description="등록 성공 (Result=1)"
            ),
            400: OpenApiResponse(
                description="등록 실패 (Result=0)"
            )
        },
    )
    def post(self, request):
        user_id = request.data.get("user_id")
        item_id = request.data.get("item_id")
        is_wishlist = request.data.get("is_wishlist") # 1: 추가, 0: 삭제


        if not user_id and user_id != 0:
            return Response({"Result": 0, "Message": "user_id가 필요합니다.", "data": ""}, status=400)
        if not item_id and item_id != 0:
            return Response({"Result": 0, "Message": "item_id가 필요합니다.", "data": ""}, status=400)
        if is_wishlist not in [0, 1]:
            return Response({"Result": 0, "Message": "is_wishlist 값은 0(삭제) 또는 1(추가)만 가능합니다.", "data": ""}, status=400)

        try:
            if is_wishlist == 1:
                # 찜 추가
                is_added = self.repository.add_wishlist(user_id, item_id)
                if is_added:
                    return Response({"Result": 1, "Message": "찜 추가됨", "data": {"is_wishlist": 1}}, status=201)
                else:
                    return Response({"Result": 0, "Message": "이미 찜한 항목입니다.", "data": ""}, status=400)

            else:
                # 찜 삭제
                is_deleted = self.repository.remove_wishlist(user_id, item_id)
                if is_deleted:
                    return Response({"Result": 1, "Message": "찜 삭제됨", "data": {"is_wishlist": 0}}, status=200)
                else:
                    return Response({"Result": 0, "Message": "찜한 항목이 아닙니다.", "data": ""}, status=400)

        except Exception as e:
            return Response({"Result": 0, "Message": str(e), "data": ""}, status=500)