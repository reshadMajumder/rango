from rango.router import Router
from .views import StudentListCreateView, StudentDetailView

router = Router()
router.add("/students", StudentListCreateView, methods=["GET", "POST"])
router.add("/students/{id}", StudentDetailView, methods=["GET", "PUT", "DELETE"])
