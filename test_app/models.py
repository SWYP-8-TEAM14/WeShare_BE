from django.db import models


class User(models.Model):
    userid = models.IntegerField(unique=True)
    username = models.CharField(max_length=50)

    class Meta:
        db_table = "user"
