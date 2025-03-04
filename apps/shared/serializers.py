from rest_framework import serializers

class ItemListRequestSerializer(serializers.Serializer):
    """
    물품 리스트 조회 시, Body로 전달하는 파라미터.
    """
    user_id = serializers.IntegerField(help_text="유저 ID")
    group_id = serializers.IntegerField(help_text="그룹 ID (전체=0)")
    sort = serializers.IntegerField(help_text="정렬 (최신순=1, 오래된순=2)")

class ItemDetailRequestSerializer(serializers.Serializer):
    """
    물품 리스트 조회 시, Body로 전달하는 파라미터.
    """
    user_id = serializers.IntegerField(help_text="유저 ID")
    item_id = serializers.IntegerField(help_text="아이템 ID")
    

class ItemDeleteRequestSerializer(serializers.Serializer):
    """
    물품 삭제 시, Body로 전달하는 파라미터.
    """
    user_id = serializers.IntegerField(help_text="유저 ID")
    item_id = serializers.IntegerField(help_text="아이템 ID")

class ItemUserListRequestSerializer(serializers.Serializer):
    """
    사용자 예약 물품 조회 시, Body로 전달하는 파라미터. 
    """
    user_id = serializers.IntegerField(help_text="유저 ID")
    group_id = serializers.IntegerField(help_text="그룹 ID (전체=0)")
    sort = serializers.IntegerField(help_text="정렬 (최신순=1, 오래된순=2)")

class ItemReserveRequestSerializer(serializers.Serializer):
    """
    사용자 물품 예약 시, Body로 전달하는 파라미터.
    """
    user_id = serializers.IntegerField(help_text="유저 ID")
    item_id = serializers.IntegerField(help_text="아이템 ID")
    rental_start = serializers.DateTimeField(help_text="대여 시간", required=True, allow_null=False)
    rental_end = serializers.DateTimeField(help_text="반납 시간", required=True, allow_null=False)

class WishListToggleRequestSerializer(serializers.Serializer):
    """
    사용자 물품 예약 시, Body로 전달하는 파라미터.
    """
    user_id = serializers.IntegerField(help_text="유저 ID")
    item_id = serializers.IntegerField(help_text="아이템 ID")
    is_wishlist = serializers.IntegerField(help_text="찜 추가/삭제 (1: 추가, 0: 삭제)")


class ItemAddSwaggerSerializer(serializers.Serializer):
    """ItemAddView - 물품 등록 시 요청 Body"""
    user_id = serializers.IntegerField()
    group_id = serializers.IntegerField()
    item_name = serializers.CharField(max_length=255)
    pickup_place = serializers.CharField(required=False, allow_blank=True)
    return_place = serializers.CharField(required=False, allow_blank=True)
    item_description = serializers.CharField(required=False, allow_blank=True)
    status = serializers.IntegerField(required=False)
    quantity = serializers.IntegerField(required=False)
    caution = serializers.CharField(required=False, allow_blank=True)
    images = serializers.ListField(child=serializers.FileField(), required=False, allow_empty=True)


class ItemListSwaggerSerializer(serializers.Serializer):
    """ItemView - 물품 리스트 조회 결과 예시"""
    group_id = serializers.IntegerField()
    group_name = serializers.CharField()
    item_id = serializers.IntegerField()
    item_name = serializers.CharField()
    item_image = serializers.CharField(allow_blank=True)
    quantity = serializers.IntegerField()
    created_at = serializers.DateTimeField(allow_null=True)
    is_wishlist = serializers.IntegerField()
    status = serializers.IntegerField()
    user_id = serializers.CharField(allow_null=True)
    user_name = serializers.CharField(allow_null=True)

class ItemDetailSwaggerSerializer(serializers.Serializer):
    """ItemDetailView - 물품 상세 조회 결과 예시"""
    user_id = serializers.IntegerField()
    group_id = serializers.IntegerField()
    group_name = serializers.CharField()
    item_id = serializers.IntegerField()
    item_name = serializers.CharField()
    item_description = serializers.CharField(allow_blank=True)
    item_image = serializers.CharField(allow_blank=True)
    status = serializers.IntegerField(help_text="물품 상태 (0: 예약 가능, 1: 예약 완료, 2: 픽업 완료)")
    quantity = serializers.IntegerField()
    caution = serializers.CharField(allow_blank=True)
    created_at = serializers.DateTimeField(allow_null=True)


class CommonResponseSerializer(serializers.Serializer):
    """모든 응답의 공통 구조 {Result, Message, data}"""
    Result = serializers.IntegerField()
    Message = serializers.CharField()
    data = serializers.CharField()
