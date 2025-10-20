from rango_api.serializers import ModelSerializer
from .models import Example, Category

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "created_at"]

class ExampleSerializer(ModelSerializer):
    class Meta:
        model = Example
        fields = ["id", "title", "description", "category", "is_active", "created_at", "updated_at"]
        nested_serializers = {
            'Category': CategorySerializer
        }
