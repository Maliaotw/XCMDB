
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from assets import views
from django.urls import path
from django.conf.urls import include
from common import views



urlpatterns = [
    path('user/', views.UserAPIView.as_view()),
]
