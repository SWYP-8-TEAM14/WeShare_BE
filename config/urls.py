from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from apps.users.auth.views import SignupView, LoginView, HomeView
from apps.users.views import UserView

urlpatterns = [
    # admin
    path("admin/", admin.site.urls),

    # apps
    path("api/v1/home/", HomeView.as_view(), name="home"),
    path("api/v1/users/", include("apps.users.urls")),
    path("api/v1/groups/", include("apps.groups.urls")),
    path('api/v1/shared/', include('apps.shared.urls')),
    path("api/v1/users/me/", UserView.as_view(), name="user"),

    # Swagger 및 API 문서
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
