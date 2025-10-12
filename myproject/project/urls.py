

from rango.router import Router
from apps.students.urls import router as students_router
from .views import HomeView

router = Router()

router.add("/", HomeView, methods=["GET"])

router.include(students_router)
