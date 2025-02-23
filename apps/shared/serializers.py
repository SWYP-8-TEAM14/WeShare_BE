from rest_framework import serializers
from .models import Item, Reservation, RentalRequest, RentalRecord

class ItemAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
                'group_id'
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

class ItemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

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

