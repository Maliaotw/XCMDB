
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import views


urlpatterns = [
    path('idrac', views.IdracSettingView.as_view()),
    path('vcenter', views.VcenterSettingView.as_view()),
    path('ldap', views.LDAPSettingView.as_view()),
]
