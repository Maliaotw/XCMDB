
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path
from django.conf.urls import include

# viewset 配置路由
router = DefaultRouter()
router.register(r'loginlog', views.LoginListViewSet)  # Allow: GET, POST, HEAD, OPTIONS



urlpatterns = [
    path('', include(router.urls)),
]
