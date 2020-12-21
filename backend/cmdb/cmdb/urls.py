from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse

urlpatterns = [
    path("", lambda x: HttpResponse("OK"), name="home"),
    path("api/", include('api.urls', namespace="api")),
    # path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    # path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    # # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # # User management
    # path("users/", include("vsphere_monitor.users.urls", namespace="users")),
    # path("accounts/", include("allauth.urls")),
]
