# rango/router.py
from starlette.routing import Route, Mount
from starlette.requests import Request
from typing import Any, Dict, List
import inspect

class Router:
    """Simple router wrapper for Rango framework."""
    def __init__(self):
        self.routes: List[Route] = []

    def add(self, path: str, view_class, methods=None):
        """
        Add a route for a view class.
        :param path: URL path
        :param view_class: View class with get/post/put/delete methods
        :param methods: List of HTTP methods
        """
        methods = methods or ["GET"]
        view_instance = view_class()

        for method in methods:
            method_upper = method.upper()
            view_method = getattr(view_instance, method_upper.lower())

            # Create a handler that can accept path parameters
            async def handler(request: Request, _method=method_upper, _view_method=view_method, _view_instance=view_instance):
                # Get the method signature to see what parameters it expects
                sig = inspect.signature(_view_method)
                params = list(sig.parameters.keys())
                
                # If the method only expects 'request', call it with just request
                if len(params) == 1 and 'request' in params:
                    return await _view_method(request)
                # If the method expects 'request' and other parameters, we need to handle path params
                elif 'request' in params and len(params) > 1:
                    # Extract path parameters from the request
                    path_params = {}
                    for param in params:
                        if param != 'request' and param in request.path_params:
                            # Convert to int if it looks like an ID
                            value = request.path_params[param]
                            if param == 'id' and value.isdigit():
                                path_params[param] = int(value)
                            else:
                                path_params[param] = value
                    return await _view_method(request, **path_params)
                else:
                    # If the method doesn't expect request, call it without parameters
                    return await _view_method()

            # Register the route with Starlette
            route = Route(path, handler, methods=[method_upper])
            self.routes.append(route)
            # Also register with trailing slash to avoid 404s
            if not path.endswith("/"):
                route_with_slash = Route(path + "/", handler, methods=[method_upper])
                self.routes.append(route_with_slash)

    def include(self, router):
        """
        Include another router.
        Accepts either a Router instance or raw Starlette routes.
        """
        if hasattr(router, "routes"):  # another Router instance
            self.routes.extend(router.routes)
        else:  # raw Starlette routes
            self.routes.extend(router)
