from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from apps.users.auth.views import SignupView, LoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    # users
    path("api/v1/", include("apps.users.urls")),
    # shared
    path("api/v1/shared", include("apps.shared.urls")),
    path("api/v1/signup/", SignupView.as_view(), name="signup"),
    path("api/v1/login/", LoginView.as_view(), name="login"),
    # Swagger 및 API 문서
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
