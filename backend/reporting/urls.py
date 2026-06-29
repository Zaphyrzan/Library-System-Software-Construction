from rest_framework.routers import DefaultRouter
from .views import FineViewSet, NotificationViewSet, ReportViewSet

router = DefaultRouter()
router.register(r"fines", FineViewSet)
router.register(r"notifications", NotificationViewSet)
router.register(r"reports", ReportViewSet, basename="reports")

urlpatterns = router.urls
