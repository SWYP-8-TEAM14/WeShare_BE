# from .models import Item, Reservation, RentalRecord, RentalRequest
# from .serializers import ItemAddSerializer, ItemListSerializer, ItemDetailSerializer, ItemReservationsSerializer, ItemReservationsListSerializer, ItemPickupSerializer, ItemReturnSerializer, ItemReturnListSerializer

# class ItemService:
    
#     @staticmethod
#     def put_item(data):
#         serializer = ItemAddSerializer(data=data)

#         if serializer.is_valid(raise_exception=True):
#             item = serializer.save()
#             return ItemAddSerializer(item).data
        
#         return {"errors": serializer.errors}

#     @staticmethod
#     def get_item_list(data):
#         item_list = Item.objects.filter(user_id=data['user_id'])

#         if not item_list.exists():
#             return None
        
#         return ItemSerializer(item_list, many=True).data
    

#     @staticmethod
#     def get_item_detail(data):
#         item = Item.objects.filter(user_id=data['user_id'])

#         if not item.exists():
#             return None
        
#         return ItemSerializer(item, many=True).data
    

#     @staticmethod
#     def item_reservations(data):
#         item = Item.objects.filter(user_id=data['user_id'])

#         if not item.exists():
#             return None
        
#         return ItemSerializer(item, many=True).data
    
    
#     @staticmethod
#     def get_item_reservations_list(data):
#         item = Item.objects.filter(user_id=data['user_id'])

#         if not item.exists():
#             return None
        
#         return ItemSerializer(item, many=True).data
    

#     @staticmethod
#     def item_pickup(data):
#         item = Item.objects.filter(user_id=data['user_id'])

#         if not item.exists():
#             return None
        
#         return ItemSerializer(item, many=True).data
    

#     @staticmethod
#     def item_return(data):
#         item = Item.objects.filter(user_id=data['user_id'])

#         if not item.exists():
#             return None
        
#         return ItemSerializer(item, many=True).data
    

#     @staticmethod
#     def get_item_return_list(data):
#         item = Item.objects.filter(user_id=data['user_id'])

#         if not item.exists():
#             return None
        
#         return ItemSerializer(item, many=True).data