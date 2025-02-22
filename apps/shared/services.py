from .models import Item, Reservation, RentalRecord, RentalRequest
from .serializers import ItemSerializer, ReservationSerializer, RentalRecordSerializer

class ItemService:
    def get_item_list(self, user_id):
        item_list = Item.objects.filter(user_id=user_id)

        if not item_list.exists():
            return None
        
        return ItemSerializer(item_list, many=True).data
    

    def get_item_detail(self, user_id):
        item = Item.objects.filter(user_id=user_id)

        if not item.exists():
            return None
        
        return ItemSerializer(item, many=True).data
    

    def item_reservations(self, user_id):
        item = Item.objects.filter(user_id=user_id)

        if not item.exists():
            return None
        
        return ItemSerializer(item, many=True).data
    
    
    def get_item_reservations_list(self, user_id):
        item = Item.objects.filter(user_id=user_id)

        if not item.exists():
            return None
        
        return ItemSerializer(item, many=True).data
    

    def item_pickup(self, user_id):
        item = Item.objects.filter(user_id=user_id)

        if not item.exists():
            return None
        
        return ItemSerializer(item, many=True).data
    

    def item_return(self, user_id):
        item = Item.objects.filter(user_id=user_id)

        if not item.exists():
            return None
        
        return ItemSerializer(item, many=True).data
    

    def get_item_return_list(self, user_id):
        item = Item.objects.filter(user_id=user_id)

        if not item.exists():
            return None
        
        return ItemSerializer(item, many=True).data