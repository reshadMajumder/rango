from rango.generics import ListCreateView, RetrieveUpdateDeleteView
from .models import Student
from .serializers import StudentSerializer

class StudentListCreateView(ListCreateView):
    model = Student
    serializer_class = StudentSerializer

    async def get(self, request, **kwargs):
        return await super().get(request)

    async def post(self, request, **kwargs):
        return await super().post(request)

class StudentDetailView(RetrieveUpdateDeleteView):
    model = Student
    serializer_class = StudentSerializer

    async def get(self, request, id: int, **kwargs):
        return await super().get(request, id)

    async def put(self, request, id: int, **kwargs):
        return await super().put(request, id)

    async def delete(self, request, id: int, **kwargs):
        return await super().delete(request, id)
