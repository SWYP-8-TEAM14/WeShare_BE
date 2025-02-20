from rest_framework import serializers
from .models import User, Item, Reservation, RentalRecord

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class RentalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalRecord
        fields = '__all__'
