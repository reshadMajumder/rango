
#rango.generics.py
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from .serializers import ModelSerializer

class ListCreateView:
    model = None
    serializer_class = None

    async def get(self, request):
        objects = await self.model.all()
        serializer = self.serializer_class(objects, many=True)
        return JSONResponse(serializer.data)

    async def post(self, request):
        data = await request.json()
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            obj = await self.model.create(**serializer.validated_data)
            return JSONResponse(self.serializer_class(obj).data)
        raise HTTPException(status_code=400, detail=serializer.errors)

class RetrieveUpdateDeleteView:
    model = None
    serializer_class = None

    async def get(self, request, id: int):
        obj = await self.model.filter(id=id).first()
        if not obj:
            raise HTTPException(status_code=404, detail="Not found")
        return JSONResponse(self.serializer_class(obj).data)

    async def put(self, request, id: int):
        obj = await self.model.filter(id=id).first()
        if not obj:
            raise HTTPException(status_code=404, detail="Not found")
        data = await request.json()
        serializer = self.serializer_class(data=data, instance=obj)
        if serializer.is_valid():
            for key, value in serializer.validated_data.items():
                setattr(obj, key, value)
            await obj.save()
            return JSONResponse(self.serializer_class(obj).data)
        raise HTTPException(status_code=400, detail=serializer.errors)

    async def delete(self, request, id: int):
        obj = await self.model.filter(id=id).first()
        if not obj:
            raise HTTPException(status_code=404, detail="Not found")
        await obj.delete()
        return JSONResponse({"detail": "Deleted"})
