from rest_framework import serializers
from api.models import Categories


class CategoriesSerializer(serializers.ModelSerializer):
    """
    Serializer for listing all categories.
    """
    class Meta:
        """
       Metadata for CategoriesSerializer.
       Contains categories model and field
       """
        model = Categories
        fields = ("id",
                  'name',
                  'icon')

