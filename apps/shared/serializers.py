from rest_framework import serializers

class ItemListRequestSerializer(serializers.Serializer):
    """
    물품 리스트 조회 시, Body로 전달하는 파라미터.
    """
    user_id = serializers.IntegerField(help_text="유저 ID")
    group_id = serializers.IntegerField(help_text="그룹 ID (전체=0)")
    sort = serializers.IntegerField(help_text="정렬 (최신순=1, 오래된순=2)")
    sort = serializers.IntegerField(help_text="정렬 (최신순=1, 오래된순=2)")
    is_all = serializers.BooleanField(help_text="전체 데이터 조회 여부 (전체=true, 부분(최대6개)=false)")

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
    item_id = serializers.ListField(child=serializers.IntegerField(), help_text="아이템 ID 리스트")

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

class ItemPickupRequestSerializer(serializers.Serializer):
    """
    사용자 물품 픽업 시, Body로 전달하는 파라미터.
    """
    user_id = serializers.IntegerField(help_text="유저 ID")
    item_id = serializers.IntegerField(help_text="아이템 ID")
    pickup_time = serializers.DateTimeField(allow_null=True)
    pickup_image = serializers.ListField(child=serializers.FileField(), required=False, allow_empty=True)

class ItemReturnRequestSerializer(serializers.Serializer):
    """
    사용자 물품 픽업 시, Body로 전달하는 파라미터.
    """
    user_id = serializers.IntegerField(help_text="유저 ID")
    item_id = serializers.IntegerField(help_text="아이템 ID")
    return_time = serializers.DateTimeField(allow_null=True)
    return_image = serializers.ListField(child=serializers.FileField(), required=False, allow_empty=True)


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

# class ItemDetailSwaggerSerializer(serializers.Serializer):
#     """ItemDetailView - 물품 상세 조회 결과 예시"""
#     user_id = serializers.IntegerField()
#     group_id = serializers.IntegerField()
#     group_name = serializers.CharField()
#     item_id = serializers.IntegerField()
#     item_name = serializers.CharField()
#     item_description = serializers.CharField(allow_blank=True)
#     item_image = serializers.CharField(allow_blank=True)
#     status = serializers.IntegerField(help_text="물품 상태 (0: 예약 가능, 1: 예약 완료, 2: 픽업 완료)")
#     quantity = serializers.IntegerField()
#     caution = serializers.CharField(allow_blank=True)
#     created_at = serializers.DateTimeField(allow_null=True)

class RentalHistorySerializer(serializers.Serializer):
    """Rental History - 대여 내역"""
    rental_start = serializers.DateTimeField()
    rental_end = serializers.DateTimeField()
    username = serializers.CharField()
    profile_image = serializers.CharField(allow_blank=True)

class ItemDetailSwaggerSerializer(serializers.Serializer):
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
    user_id = serializers.IntegerField(allow_null=True)
    user_name = serializers.CharField(allow_null=True)
    rental_history = RentalHistorySerializer(many=True, required=False)  # rental_history 추가

class CommonResponseSerializer(serializers.Serializer):
    """모든 응답의 공통 구조 {Result, Message, data}"""
    Result = serializers.IntegerField()
    Message = serializers.CharField()
    data = serializers.CharField()
    

class ItemDetailDataSerializer(serializers.Serializer):
    """물품 상세 정보의 구조"""
    user_id = serializers.IntegerField(help_text="등록한 사용자 ID")
    username = serializers.CharField(help_text="사용자 이름")
    group_id = serializers.IntegerField(help_text="그룹 ID")
    group_name = serializers.CharField(help_text="그룹 이름")
    item_id = serializers.IntegerField(help_text="물품 ID")
    item_name = serializers.CharField(help_text="물품 이름")
    pickup_place = serializers.CharField(help_text="픽업 장소", allow_blank=True)
    return_place = serializers.CharField(help_text="반납 장소", allow_blank=True)
    item_description = serializers.CharField(help_text="물품 설명", allow_blank=True)
    image_urls = serializers.ListField(child=serializers.CharField(), help_text="이미지 URL 리스트")
    status = serializers.IntegerField(help_text="물품 상태")
    quantity = serializers.IntegerField(help_text="수량")
    caution = serializers.CharField(help_text="주의사항", allow_blank=True)
    created_at = serializers.DateTimeField(help_text="등록일")

class ItemDetailResponseSerializer(CommonResponseSerializer):
    """공통 응답 구조 + 물품 상세 조회 `data` 필드의 구체적인 구조"""
    data = ItemDetailDataSerializer(help_text="물품 상세 정보")

class ItemListDataSerializer(serializers.Serializer):
    """물품 리스트의 단일 아이템 데이터 구조"""
    group_id = serializers.IntegerField(help_text="그룹 ID")
    group_name = serializers.CharField(help_text="그룹 이름")
    item_id = serializers.IntegerField(help_text="물품 ID")
    item_name = serializers.CharField(help_text="물품 이름")
    image_urls = serializers.ListField(child=serializers.CharField(), help_text="이미지 URL 리스트")
    quantity = serializers.IntegerField(help_text="수량")
    created_at = serializers.DateTimeField(help_text="등록일")
    is_wishlist = serializers.IntegerField(help_text="찜 여부 (1: 찜, 0: 안함)")
    status = serializers.IntegerField(help_text="물품 상태")
    reservation_user_id = serializers.IntegerField(help_text="예약자 ID", allow_null=True)
    reservation_user_name = serializers.CharField(help_text="예약자 이름", allow_null=True)

class ItemListResponseSerializer(CommonResponseSerializer):
    """공통 응답 구조 + 물품 리스트 조회 `data` 필드의 구조"""
    data = serializers.ListField(child=ItemListDataSerializer(), help_text="물품 목록 데이터")

class ItemReserveDataSerializer(serializers.Serializer):
    """물품 예약 정보 데이터 구조"""
    item_id = serializers.IntegerField(help_text="예약된 물품 ID")
    rental_start = serializers.DateTimeField(help_text="대여 시작 시간")
    rental_end = serializers.DateTimeField(help_text="반납 예정 시간")

class ItemReserveResponseSerializer(CommonResponseSerializer):
    """공통 응답 구조 + 물품 예약 응답 `data` 필드의 구조"""
    data = ItemReserveDataSerializer(help_text="예약된 물품 정보")

class ItemReserveListDataSerializer(serializers.Serializer):
    """예약한 물품 리스트의 단일 아이템 데이터 구조"""
    group_id = serializers.IntegerField(help_text="그룹 ID")
    group_name = serializers.CharField(help_text="그룹 이름")
    item_id = serializers.IntegerField(help_text="물품 ID")
    item_name = serializers.CharField(help_text="물품 이름")
    image_urls = serializers.ListField(child=serializers.CharField(), help_text="이미지 URL 리스트")
    quantity = serializers.IntegerField(help_text="수량")
    created_at = serializers.DateTimeField(help_text="등록일")
    status = serializers.IntegerField(help_text="물품 상태")
    rental_start = serializers.DateTimeField(help_text="대여 시작 시간")
    rental_end = serializers.DateTimeField(help_text="반납 예정 시간")
    is_wishlist = serializers.IntegerField(help_text="찜 여부 (1: 찜, 0: 안함)")
    reservation_user_id = serializers.IntegerField(help_text="예약자 ID", allow_null=True)
    reservation_user_name = serializers.CharField(help_text="예약자 이름", allow_null=True)

class ItemReserveListResponseSerializer(CommonResponseSerializer):
    """공통 응답 구조 + 사용자 예약 물품 목록 조회 `data` 필드의 구조"""
    data = serializers.ListField(child=ItemReserveListDataSerializer(), help_text="예약된 물품 목록 데이터")

class ItemPickupDataSerializer(serializers.Serializer):
    """픽업 인증 데이터 구조"""
    user_id = serializers.IntegerField(help_text="사용자 ID")
    item_id = serializers.IntegerField(help_text="픽업한 물품 ID")
    rental_start = serializers.DateTimeField(help_text="대여 시작 시간")
    rental_end = serializers.DateTimeField(help_text="반납 예정 시간")

class ItemPickupResponseSerializer(CommonResponseSerializer):
    """공통 응답 구조 + 픽업 인증 응답 `data` 필드의 구조"""
    data = ItemPickupDataSerializer(help_text="픽업된 물품 정보")

class ItemReturnableListDataSerializer(serializers.Serializer):
    """반납 가능한 물품 리스트의 단일 아이템 데이터 구조"""
    user_id = serializers.IntegerField(help_text="사용자 ID")
    group_id = serializers.IntegerField(help_text="그룹 ID")
    group_name = serializers.CharField(help_text="그룹 이름")
    item_id = serializers.IntegerField(help_text="물품 ID")
    item_name = serializers.CharField(help_text="물품 이름")
    item_description = serializers.CharField(help_text="물품 설명", allow_blank=True)
    image_urls = serializers.ListField(child=serializers.CharField(), help_text="이미지 URL 리스트")
    item_status = serializers.IntegerField(help_text="물품 상태")
    quantity = serializers.IntegerField(help_text="수량")
    caution = serializers.CharField(help_text="주의사항", allow_blank=True)
    rental_start = serializers.DateTimeField(help_text="대여 시작 시간")
    rental_end = serializers.DateTimeField(help_text="반납 예정 시간")

class ItemReturnableListResponseSerializer(CommonResponseSerializer):
    """공통 응답 구조 + 반납 가능 물품 목록 조회 `data` 필드의 구조"""
    data = serializers.ListField(child=ItemReturnableListDataSerializer(), help_text="반납 가능한 물품 목록 데이터")

class ItemReturnDataSerializer(serializers.Serializer):
    """반납 인증 데이터 구조"""
    user_id = serializers.IntegerField(help_text="사용자 ID")
    item_id = serializers.IntegerField(help_text="반납한 물품 ID")
    rental_start = serializers.DateTimeField(help_text="대여 시작 시간")
    rental_end = serializers.DateTimeField(help_text="반납 예정 시간")

class ItemReturnResponseSerializer(CommonResponseSerializer):
    """공통 응답 구조 + 반납 인증 응답 `data` 필드의 구조"""
    data = ItemReturnDataSerializer(help_text="반납된 물품 정보")

class WishlistToggleDataSerializer(serializers.Serializer):
    """찜 토글(추가/삭제) 데이터 구조"""
    is_wishlist = serializers.IntegerField(help_text="찜 여부 (1: 추가, 0: 삭제)")

class WishlistToggleResponseSerializer(CommonResponseSerializer):
    """공통 응답 구조 + 찜 추가/삭제 응답 `data` 필드의 구조"""
    data = WishlistToggleDataSerializer(help_text="찜 상태 정보")