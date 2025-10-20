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

        async def lifespan(app):
            # Startup: initialize DB
            try:
                from .db import init_db
                await init_db()
            except Exception as e:
                print(f"Database initialization error: {e}")
            yield
            # Shutdown: close DB
            try:
                from .db import close_db
                await close_db()
            except Exception as e:
                print(f"Database close error: {e}")

        # Initialize Starlette with empty routes and middleware and lifespan
        super().__init__(routes=[], middleware=[], lifespan=lifespan)

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
        """Add middleware directly to the Starlette app."""
        super().add_middleware(middleware_class, **options)

    def _build_app_with_middleware(self):
        """No-op: middleware is applied directly to this app."""
        return self

    # Use Starlette's default __call__ with lifespan; no override needed

    def run(self, host="127.0.0.1", port=8000):
        import uvicorn
        # Use the app with middleware applied
        app_with_middleware = self._build_app_with_middleware()
        uvicorn.run(app_with_middleware, host=host, port=port)
