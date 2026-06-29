from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, CategoryViewSet, BookViewSet, BookCopyViewSet

router = DefaultRouter()
router.register(r"authors", AuthorViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"books", BookViewSet)
router.register(r"copies", BookCopyViewSet)

urlpatterns = router.urls
