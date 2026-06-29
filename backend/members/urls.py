from rest_framework.routers import DefaultRouter
from .views import MembershipViewSet, MemberViewSet, StaffViewSet

router = DefaultRouter()
router.register(r"memberships", MembershipViewSet)
router.register(r"members", MemberViewSet)
router.register(r"staff", StaffViewSet)

urlpatterns = router.urls
