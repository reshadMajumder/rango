from rango_api.router import Router
from .views import HomeView
from apps.joo.urls import router as joo_router

router = Router()
router.add("/", HomeView, methods=["GET"])

router.include(joo_router)
