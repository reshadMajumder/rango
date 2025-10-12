import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))  # Adds E:\personal-projects\rango

from rango.core import RangoApp
from rango.middleware import SimpleCORSMiddleware
from project.urls import router

app = RangoApp(debug=True)
app.add_middleware(SimpleCORSMiddleware)
app.include_router(router)

# Add startup event handler for database initialization
@app.on_event("startup")
async def startup_event():
    from rango.db import init_db
    await init_db()
