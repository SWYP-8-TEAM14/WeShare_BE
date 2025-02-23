from django.urls import path, include
from .views import ItemAddView, ItemView, ItemDetailView, ItemReservationsView, ItemReservationsListView, ItemPickupView, ItemReturnView, ItemReturnListView

urlpatterns = [
    path("items/add", ItemAddView.as_view()),
    path("items/", ItemView.as_view()),
    path("items/detail/", ItemDetailView.as_view()),
    path("items/reservations/", ItemReservationsView.as_view()),
    path("items/reservations/list/", ItemReservationsListView.as_view()),
    path("items/pickup/", ItemPickupView.as_view()),
    path("items/return/", ItemReturnView.as_view()),
    path("items/return/list/", ItemReturnListView.as_view()),
]
