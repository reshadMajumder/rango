
from rango.serializers import ModelSerializer
from .models import Student

class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name", "email", "age", "created_at"]
