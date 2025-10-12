from rango.generics import ListCreateView
from fastapi.responses import JSONResponse

class HomeView:
    async def get(self, request):
        return JSONResponse({"message": "Welcome to Rango Framework!"})
