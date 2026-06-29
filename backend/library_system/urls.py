from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/catalog/", include("catalog.urls")),
    path("api/members/", include("members.urls")),
    path("api/circulation/", include("circulation.urls")),
    path("api/reservations/", include("reservations.urls")),
    path("api/reporting/", include("reporting.urls")),
]
