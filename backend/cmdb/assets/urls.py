
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from assets import views
from django.urls import path
from django.conf.urls import include
from assets import views

# viewset 配置路由
router = DefaultRouter()
router.register(r'assets', views.AssetsModelViewSet)  # Allow: GET, POST, HEAD, OPTIONS
router.register(r'tag', views.TAGModelViewSet)  # Allow: GET, POST, HEAD, OPTIONS
router.register(r'idc', views.IDCModelViewSet)  # Allow: GET, POST, HEAD, OPTIONS
router.register(r'isp', views.ISPModelViewsSet)  # Allow: GET, POST, HEAD, OPTIONS
router.register(r'netdevice', views.NetDeviceModelViewsSet)  # Allow: GET, POST, HEAD, OPTIONS
router.register(r'rack', views.RackModelViewSet)  # Allow: GET, POST, HEAD, OPTIONS
router.register(r'rackunit', views.RackUnitModelViewSet)  # Allow: GET, POST, HEAD, OPTIONS
router.register(r'storage', views.StorageModelViewsSet)  # Allow: GET, POST, HEAD, OPTIONS


urlpatterns = [
    path('', include(router.urls)),
    path(r'assets/type', views.AssetTypeAPIView.as_view()),
    path(r'assets/status', views.AssetStatusAPIView.as_view()),
    path(r'netdevice/type', views.NetdeviceStatusAPIView.as_view()),
    # path(r'rack/type', views.NetDriveTypeAPIView.as_view()),
    path(r'rack/detail/<int:pk>', views.RackDetailAPIView.as_view()),
]
