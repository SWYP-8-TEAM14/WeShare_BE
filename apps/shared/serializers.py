from rest_framework import serializers

class ItemListRequestSerializer(serializers.Serializer):
    """
    물품 리스트 조회 시, Body로 전달하는 파라미터.
    """
    user_id = serializers.IntegerField(help_text="유저 ID")

class ItemDetailRequestSerializer(serializers.Serializer):
    """
    물품 리스트 조회 시, Body로 전달하는 파라미터.
    """
    user_id = serializers.IntegerField(help_text="유저 ID")
    item_id = serializers.IntegerField(help_text="아이템 ID")


class ItemAddSwaggerSerializer(serializers.Serializer):
    """ItemAddView - 물품 등록 시 요청 Body"""
    user_id = serializers.IntegerField()
    group_id = serializers.IntegerField()
    item_name = serializers.CharField(max_length=255)
    item_description = serializers.CharField(required=False, allow_blank=True)
    item_image = serializers.CharField(required=False, allow_blank=True)
    status = serializers.IntegerField(required=False)
    quantity = serializers.IntegerField(required=False)
    caution = serializers.CharField(required=False, allow_blank=True)
    created_at = serializers.DateTimeField(required=False, allow_null=True)
    deleted_at = serializers.DateTimeField(required=False, allow_null=True)


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
    reservation_user_id = serializers.CharField(allow_null=True)
    reservation_user_name = serializers.CharField(allow_null=True)

class ItemDetailSwaggerSerializer(serializers.Serializer):
    """ItemDetailView - 물품 상세 조회 결과 예시"""
    user_id = serializers.IntegerField()
    group_id = serializers.IntegerField()
    group_name = serializers.CharField()
    item_id = serializers.IntegerField()
    item_name = serializers.CharField()
    item_description = serializers.CharField(allow_blank=True)
    item_image = serializers.CharField(allow_blank=True)
    status = serializers.IntegerField()
    quantity = serializers.IntegerField()
    caution = serializers.CharField(allow_blank=True)
    created_at = serializers.DateTimeField(allow_null=True)


class CommonResponseSerializer(serializers.Serializer):
    """모든 응답의 공통 구조 {Result, Message, data}"""
    Result = serializers.IntegerField()
    Message = serializers.CharField()
    data = serializers.CharField()
