from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# ---- Swagger / ReDoc API 文檔 ----
schema_view = get_schema_view(
    openapi.Info(
        title="XCMDB API",
        default_version="v1",
        description="XCMDB IT 資產管理系統 API 文檔",
        contact=openapi.Contact(email="admin@xcmdb.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", lambda x: HttpResponse("OK"), name="home"),
    path("api/", include("api.urls", namespace="api")),
    # path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    # path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    # # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # # User management
    # path("users/", include("vsphere_monitor.users.urls", namespace="users")),
    # path("accounts/", include("allauth.urls")),
    # ---- API 文檔 ----
    path("api/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
