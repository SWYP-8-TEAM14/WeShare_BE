from django.urls import path
from .views import (
    ItemView,
    ItemAddView,
    ItemDeleteView,
    ItemDetailView,
    ItemReserveView,
    ItemReserveListView,
    ItemPickupView,
    ItemReturnableListView,
    ItemReturnView,
    WishlistToggleView
)

urlpatterns = [
    path("items/", ItemView.as_view()),
    path("items/add", ItemAddView.as_view()),
    path("items/delete", ItemDeleteView.as_view()),
    path("items/detail/", ItemDetailView.as_view()),
    path("items/reserve", ItemReserveView.as_view()),
    path("items/reserve/list", ItemReserveListView.as_view()),
    path("items/pickup", ItemPickupView.as_view()),
    path("items/return/list", ItemReturnableListView.as_view()),
    path("items/return", ItemReturnView.as_view()),
    path("wishlist/", WishlistToggleView.as_view()),
]
