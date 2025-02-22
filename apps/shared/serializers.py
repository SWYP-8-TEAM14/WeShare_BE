from rest_framework import serializers
from .models import User, Item, Reservation, RentalRecord

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

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class RentalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalRecord
        fields = '__all__'
