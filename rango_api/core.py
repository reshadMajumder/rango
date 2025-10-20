#rango/core.py
from starlette.applications import Starlette
from starlette.middleware import Middleware
from .router import Router

class RangoApp(Starlette):
    """Main Rango app wrapper."""
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.router_obj = Router()
        self._router_mounted = False
        self._middleware_list = []
        self._db_initialized = False
        
        # Initialize Starlette with empty routes and middleware
        super().__init__(routes=[], middleware=[])

    def add_view(self, path: str, view_class, methods=None):
        self.router_obj.add(path, view_class, methods or ["GET"])

    def include_router(self, router):
        """Include a router and mount it to the Starlette app."""
        self.router_obj.include(router)
        # Mount the router to the Starlette app only once
        if not self._router_mounted:
            # Add all routes from router_obj to the Starlette app
            self.routes.extend(self.router_obj.routes)
            self._router_mounted = True

    def add_middleware(self, middleware_class, **options):
        """Add middleware to the Starlette app."""
        # Store middleware for later application
        middleware = Middleware(middleware_class, **options)
        self._middleware_list.append(middleware)

    def _build_app_with_middleware(self):
        """Build a new Starlette app with all middleware applied."""
        if not self._middleware_list:
            return self
        
        # Get current routes
        current_routes = list(self.routes)
        
        # Create new Starlette app with middleware
        return Starlette(routes=current_routes, middleware=self._middleware_list)

    async def __call__(self, scope, receive, send):
        """ASGI callable with database initialization."""
        # Initialize database on first request if not already done
        if not self._db_initialized:
            try:
                from .db import init_db
                await init_db()
                self._db_initialized = True
            except Exception as e:
                print(f"Database initialization error: {e}")
        
        # Use the app with middleware applied
        app_with_middleware = self._build_app_with_middleware()
        await app_with_middleware(scope, receive, send)

    def run(self, host="127.0.0.1", port=8000):
        import uvicorn
        # Use the app with middleware applied
        app_with_middleware = self._build_app_with_middleware()
        uvicorn.run(app_with_middleware, host=host, port=port)
