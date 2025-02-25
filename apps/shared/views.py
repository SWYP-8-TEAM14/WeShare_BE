import json
from django.db import connection
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiResponse

from .repository import ItemRepository
from .serializers import (
    ItemAddSwaggerSerializer,
    ItemListSwaggerSerializer,
    ItemDetailSwaggerSerializer,
    CommonResponseSerializer,
    ItemListRequestSerializer,
    ItemDetailRequestSerializer
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
        description="신규 물품을 등록합니다.",
        request=ItemAddSwaggerSerializer,
        responses={
            201: OpenApiResponse(
                response=CommonResponseSerializer,
                description="등록 성공 (Result=1)"
            ),
            400: OpenApiResponse(
                response=CommonResponseSerializer,
                description="등록 실패 (Result=0)"
            )
        },
    )
    def post(self, request):
        data = request.data
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
        request=None,
        responses={
            200: OpenApiResponse(description="삭제 성공/실패 여부 반환"),
            400: OpenApiResponse(description="에러")
        }
    )
    def post(self, request):
        item_id = request.data.get("item_id")
        if not item_id and item_id != 0:
            return Response({"Result":0,"Message":"item_id가 필요합니다.","data":""}, status=400)

        deleted_count = self.repository.delete_item(int(item_id))
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
                response=CommonResponseSerializer,
                description="조회 성공 (Result=1)"
            ),
            400: OpenApiResponse(
                response=CommonResponseSerializer,
                description="조회 실패 (Result=0)"
            )
        },
    )
    def post(self, request):
        user_id = request.data.get("user_id")
        if not user_id and user_id != 0:
            return Response({
                "Result": 0,
                "Message": "user_id가 필요합니다.",
                "data": ""
            }, status=400)

        try:
            result_list = self.repository.get_item_list(int(user_id))
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
                response=CommonResponseSerializer,
                description="조회 성공 (Result=1)"
            ),
            400: OpenApiResponse(
                response=CommonResponseSerializer,
                description="조회 실패 (Result=0)"
            ),
            404: OpenApiResponse(
                response=CommonResponseSerializer,
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
            detail_data = self.repository.get_item_detail(int(user_id), int(item_id))
        except Exception as e:
            return Response({"Result": 0, "Message": str(e), "data": ""}, status=400)

        if not detail_data:
            return Response({"Result": 0, "Message": "해당 데이터가 존재하지 않습니다.", "data": ""}, status=404)

        return Response({
            "Result": 1,
            "Message": "",
            "data": json.dumps(detail_data, default=str)
        }, status=200)


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
        description="RESERVATIONS 테이블에 새 레코드를 삽입합니다.",
        request=None,
        responses={
            200: OpenApiResponse(description="예약 성공 (Result=1)"),
            400: OpenApiResponse(description="에러 (Result=0)")
        }
    )
    def post(self, request):
        user_id = request.data.get("user_id")
        item_id = request.data.get("item_id")
        start_time = request.data.get("start_time")
        end_time   = request.data.get("end_time")

        if not user_id and user_id != 0:
            return Response({"Result":0,"Message":"필수필드(user_id, item_id, start_time, end_time) 누락","data":""}, status=400)
        if not item_id and item_id != 0:
            return Response({"Result":0,"Message":"필수필드(user_id, item_id, start_time, end_time) 누락","data":""}, status=400)
        if not start_time or not end_time:
            return Response({"Result":0,"Message":"필수필드(user_id, item_id, start_time, end_time) 누락","data":""}, status=400)

        try:
            self.repository.reserve_item(int(user_id), int(item_id), start_time, end_time)
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
        summary="예약 물품 조회",
        description="특정 user_id가 예약한 물품 목록을 조회합니다.",
        request=None,
        responses={
            200: OpenApiResponse(description="조회 성공 (Result=1)"),
            400: OpenApiResponse(description="오류 (Result=0)")
        }
    )
    def post(self, request):
        user_id = request.data.get("user_id")
        if not user_id and user_id != 0:
            return Response({"Result":0,"Message":"user_id가 필요합니다.","data":""}, status=400)

        try:
            rows = self.repository.get_reserved_items(int(user_id))
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
        request=None,
        responses={
            200: OpenApiResponse(description="픽업 성공"),
            400: OpenApiResponse(description="에러"),
            404: OpenApiResponse(description="예약 내역 없음")
        }
    )
    def post(self, request):
        user_id = request.data.get("user_id")
        item_id = request.data.get("item_id")
        pickup_time = request.data.get("pickup_time")
        image = request.data.get("image","")

        if not user_id and user_id != 0:
            return Response({"Result":0,"Message":"(user_id, item_id, pickup_time)는 필수입니다.","data":""}, status=400)
        if not item_id and item_id != 0:
            return Response({"Result":0,"Message":"(user_id, item_id, pickup_time)는 필수입니다.","data":""}, status=400)
        if not pickup_time:
            return Response({"Result":0,"Message":"(user_id, item_id, pickup_time)는 필수입니다.","data":""}, status=400)

        try:
            result = self.repository.pickup_item(int(user_id), int(item_id), pickup_time, image)
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
            200: OpenApiResponse(description="조회 성공 (Result=1)"),
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
