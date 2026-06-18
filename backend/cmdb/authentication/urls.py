from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

# viewset 配置路由
router = DefaultRouter()
router.register(r"loginlog", views.LoginListViewSet)  # Allow: GET, POST, HEAD, OPTIONS
router.register(r"user", views.UserModelViewSet)
router.register(r"role-permission", views.RolePermissionModelViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("jwt/token/refresh/", views.JWTRefreshTokenView.as_view(), name="jwt-token-refresh"),
]
