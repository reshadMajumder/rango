from rango_api.generics import ListCreateView
from starlette.responses import JSONResponse

class HomeView:
    async def get(self, request):
        return JSONResponse({"message": "Welcome to Rango Framework!"})
