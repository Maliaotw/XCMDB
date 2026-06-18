from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

# viewset 配置路由
router = DefaultRouter()
router.register(r"pt", views.PeriodicTaskListViewSet)  # Allow: GET, OPTIONS
router.register(r"td", views.TaskResultListViewSet)  # Allow: GET, OPTIONS


urlpatterns = [
    path("", include(router.urls)),
]
