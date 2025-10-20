from rango_api.router import Router
from .views import ExampleListCreateView, ExampleDetailView, CategoryListCreateView, CategoryDetailView

router = Router()
# Category endpoints
router.add("/categories", CategoryListCreateView, methods=["GET", "POST"])
router.add("/categories/{id}", CategoryDetailView, methods=["GET", "PUT", "PATCH", "DELETE"])
# Example endpoints
router.add("/examples", ExampleListCreateView, methods=["GET", "POST"])
router.add("/examples/{id}", ExampleDetailView, methods=["GET", "PUT", "PATCH", "DELETE"])
