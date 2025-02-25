# Generated by Django 5.1.6 on 2025-02-25 12:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("groups", "__first__"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Item",
            fields=[
                ("item_id", models.AutoField(primary_key=True, serialize=False)),
                ("item_name", models.CharField(max_length=255)),
                ("item_description", models.TextField(blank=True, null=True)),
                ("item_image", models.TextField(blank=True, null=True)),
                ("status", models.IntegerField(default=1)),
                ("quantity", models.IntegerField(default=1)),
                ("caution", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(blank=True, null=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="items", to="groups.group"
                    ),
                ),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="users.user")),
            ],
        ),
        migrations.CreateModel(
            name="RentalRecord",
            fields=[
                ("rental_id", models.AutoField(primary_key=True, serialize=False)),
                ("rental_start", models.DateTimeField()),
                ("rental_end", models.DateTimeField()),
                ("actual_return", models.DateTimeField(blank=True, null=True)),
                ("rental_status", models.CharField(max_length=50)),
                ("created_at", models.DateTimeField(blank=True, null=True)),
                ("item", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="shared.item")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="users.user")),
            ],
        ),
        migrations.CreateModel(
            name="RentalRequest",
            fields=[
                ("request_id", models.AutoField(primary_key=True, serialize=False)),
                ("requested_at", models.DateTimeField(blank=True, null=True)),
                ("item", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="shared.item")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="users.user")),
            ],
        ),
        migrations.CreateModel(
            name="Reservation",
            fields=[
                ("reservation_id", models.AutoField(primary_key=True, serialize=False)),
                ("reservation_date", models.DateTimeField(blank=True, null=True)),
                ("status", models.CharField(max_length=50)),
                ("created_at", models.DateTimeField(blank=True, null=True)),
                ("item", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="shared.item")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="users.user")),
            ],
        ),
    ]
