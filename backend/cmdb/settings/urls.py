from django.urls import path

from . import views

urlpatterns = [
    path("idrac", views.IdracSettingView.as_view()),
    path("vcenter", views.VcenterSettingView.as_view()),
    path("ldap", views.LDAPSettingView.as_view()),
]
