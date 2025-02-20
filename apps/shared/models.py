from django.db import models
from apps.users.models import User

class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    # group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    item_description = models.TextField(null=True, blank=True)
    item_image = models.TextField(null=True, blank=True)
    status = models.IntegerField(default=1)  # 1: 사용 가능, 0: 대여 중
    quantity = models.IntegerField(default=1)
    caution = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Reservation(models.Model):
    book_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    book_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)  # '예약 완료', '취소됨' 등

class RentalRecord(models.Model):
    rental_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    rental_start = models.DateTimeField()
    rental_end = models.DateTimeField()
    actual_return = models.DateTimeField(null=True, blank=True)
    rental_status = models.CharField(max_length=50)  # '대여 중', '반납 완료'
    created_at = models.DateTimeField(auto_now_add=True)