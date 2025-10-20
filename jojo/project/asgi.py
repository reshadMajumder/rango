import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from rango_api.core import RangoApp
from rango_api.middleware import SimpleCORSMiddleware
from project.urls import router

app = RangoApp(debug=True)
app.add_middleware(SimpleCORSMiddleware)
app.include_router(router)
