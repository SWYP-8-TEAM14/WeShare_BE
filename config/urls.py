from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # admin
    path("admin/", admin.site.urls),

    # apps
    path("api/v1/users/", include("apps.users.urls")),
    path('api/v1/shared/', include('apps.shared.urls')),

    # Swagger 및 API 문서
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
