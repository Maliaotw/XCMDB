
from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path
from django.conf.urls import include

from . import tasks

# viewset 配置路由
router = DefaultRouter()
# router.register(r'instance', views.VMModelViewSet)  # Allow: GET, POST, HEAD, OPTIONS
router.register(r'cluster', views.ClusterModelViewSet)  # Allow: GET, POST, HEAD, OPTIONS
router.register(r'datastore', views.DataStoreModelViewSet)  # Allow: GET, POST, HEAD, OPTIONS
router.register(r'network', views.NetWorkModelViewSet)  # Allow: GET, POST, HEAD, OPTIONS
router.register(r'netstatic', views.NetWorkStaticModelViewSet)  # Allow: GET, POST, HEAD, OPTIONS
router.register(r'instance', views.InstanceViewSet)  # Allow: GET, POST, HEAD, OPTIONS
router.register(r'instancename', views.InstanceNameViewSet)  # Allow: GET
router.register(r'host', views.HostViewSet)  # Allow: GET, POST, HEAD, OPTIONS

urlpatterns = [
    path('', include(router.urls)),
    path(r'instancelist', views.InstanceListView.as_view()),
    # path(r'vm/echo_once', views.echo_once),
]
