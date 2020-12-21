
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from hosts import views
from django.urls import path
from django.conf.urls import include

# viewset 配置路由
router = DefaultRouter()
router.register(r'hosts', views.HostModelViewSet)  # Allow: GET, POST, HEAD, OPTIONS
router.register(r'node', views.NodeModelViewSet)  # Allow: GET, POST, HEAD, OPTIONS
router.register(r'hostrecord', views.HostRecordViewSet)  # Allow: GET, POST, HEAD, OPTIONS
router.register(r'idrac', views.IdracViewSet)  # Allow: GET, POST, HEAD, OPTIONS
router.register(r'cmdrecord', views.CmdRecordViewSet)  # Allow: GET, POST, HEAD, OPTIONS
router.register(r'runuser', views.RunUserViewSet)  # Allow: GET, POST, HEAD, OPTIONS
router.register(r'process', views.ProcessViewSet)  # Allow: GET, POST, HEAD, OPTIONS
router.register(r'hostproc', views.HostProcViewSet)  # Allow: GET, POST, HEAD, OPTIONS
router.register(r'busunit', views.BusUnitModelViewSet)  # Allow: GET, POST, HEAD, OPTIONS


urlpatterns = [
    path('', include(router.urls)),
]
