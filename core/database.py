from django.db.models import QuerySet

class Repository:
    @staticmethod
    def get_objects(queryset: QuerySet, **filters):
        """
        Retrieve objects from a QuerySet with optional filters.
        """
        return queryset.filter(**filters)

    @staticmethod
    def get_object_or_none(queryset: QuerySet, **filters):
        """
        Retrieve a single object or return None if not found.
        """
        try:
            return queryset.get(**filters)
        except queryset.model.DoesNotExist:
            return None

    @staticmethod
    def create_object(queryset: QuerySet, **data):
        """
        Create a new object in the database.
        """
        return queryset.create(**data)

    @staticmethod
    def update_object(instance, **data):
        """
        Update fields of an existing object.
        """
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    @staticmethod
    def delete_object(instance):
        """
        Delete an object from the database.
        """
        instance.delete()