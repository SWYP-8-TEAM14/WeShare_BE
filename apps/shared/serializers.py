import json
from rest_framework import serializers
from apps.users.models import User
from apps.groups.models import Group
from .models import Item, Reservation, RentalRequest, RentalRecord


class ItemAddSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    group_id = serializers.IntegerField()

    class Meta:
        model = Item
        fields = [
            "user_id",
            "group_id",
            "item_name",
            "item_description",
            "item_image",
            "quantity",
            "caution",
            "created_at",
            "deleted_at",
        ]
        # item_id는 'AutoField(primary_key=True)'이므로 입력받을 필요가 없으니 제외

    def validate_status(self, value):
        """status는 0(대여 중) 또는 1(사용 가능)만 허용한다고 가정"""
        if value not in (0, 1):
            raise serializers.ValidationError("status는 0 또는 1만 가능합니다.")
        return value

    def create(self, validated_data):
        # user_id, group_id 추출
        user_id = validated_data.pop("user_id")
        group_id = validated_data.pop("group_id")

        # ForeignKey 객체 조회
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError({"user_id": "존재하지 않는 user_id 입니다."})

        try:
            group = Group.objects.get(group_id=group_id)
        except Group.DoesNotExist:
            raise serializers.ValidationError({"group_id": "존재하지 않는 group_id 입니다."})

        # 나머지 필드로 Item 생성
        item = Item.objects.create(
            user=user,
            group=group,
            **validated_data
        )
        return item

class ItemListSerializer(serializers.ModelSerializer):
    group_name = serializers.SerializerMethodField()
    is_wishlist = serializers.SerializerMethodField()
    reservation_user_id = serializers.SerializerMethodField()
    reservation_user_name = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = [
                'group'
                , 'group_name'
                , 'item_id'
                , 'item_name'
                , 'item_image'
                , 'quantity'
                , 'created_at'
                , 'is_wishlist'
                , 'status'
                , 'reservation_user_id'
                , 'reservation_user_name'
        ]

    def get_group_name(self, obj):
        return obj.group.group_name

    def get_is_wishlist(self, obj):
        # 실제로 wish list 기능이 없다면, 0(또는 False)로 임의 반환
        return 0

    def get_reservation_user_id(self, obj):
        # 예약 유저 정보가 필요하다면 Reservation 테이블을 조회하는 로직을 넣을 수 있음
        return None

    def get_reservation_user_name(self, obj):
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # group -> group_id로 key 변경
        data["group_id"] = data.pop("group")
        return data

class ItemDetailSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    group_name = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = [
            "user_id",
            "group",             # => group_id로 바꿔줄 예정
            "group_name",
            "item_id",
            "item_name",
            "item_description",
            "item_image",
            "status",
            "quantity",
            "caution",
            "created_at",
        ]

    def get_user_id(self, obj):
        return obj.user.id

    def get_group_name(self, obj):
        return obj.group.group_name

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # group -> group_id 변경
        data["group_id"] = data.pop("group")
        return data

class ItemReservationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class ItemReservationsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class ItemPickupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class ItemReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class ItemReturnListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

