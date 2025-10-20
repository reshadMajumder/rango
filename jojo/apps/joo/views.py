from rango_api.generics import ListCreateView, RetrieveUpdateDeleteView
from .models import Example, Category
from .serializers import ExampleSerializer, CategorySerializer

class CategoryListCreateView(ListCreateView):
    model = Category
    serializer_class = CategorySerializer

class CategoryDetailView(RetrieveUpdateDeleteView):
    model = Category
    serializer_class = CategorySerializer

class ExampleListCreateView(ListCreateView):
    model = Example
    serializer_class = ExampleSerializer
    select_related = ['category']  # Optimize foreign key queries

class ExampleDetailView(RetrieveUpdateDeleteView):
    model = Example
    serializer_class = ExampleSerializer
    select_related = ['category']  # Optimize foreign key queries
