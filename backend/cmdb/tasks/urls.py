
from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path
from django.conf.urls import include

# viewset 配置路由
router = DefaultRouter()
router.register(r'pt', views.PeriodicTaskListViewSet)  # Allow: GET, OPTIONS
router.register(r'td', views.TaskResultListViewSet)  # Allow: GET, OPTIONS



urlpatterns = [
    path('', include(router.urls)),
]
