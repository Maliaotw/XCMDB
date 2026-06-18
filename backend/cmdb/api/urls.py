from django.contrib import admin
from django.urls import include, path

from authentication.views import AssetData, ObtainExpiringAuthToken

from .views import DashBoardView, api_refresh_asset

app_name = "api"

api_v1 = [
    path("admin/", admin.site.urls),
    # path('ws/', echo_once),
    path("", include("assets.urls")),
    path("", include("hosts.urls")),
    path("", include("vm.urls")),
    path("", include("tasks.urls")),
    path("", include("authentication.urls")),
    path("idrac/refresh_asset", api_refresh_asset, name="idrac-refresh-asset"),
    path("assetdata/", AssetData.as_view(), name="assetdata"),
    path("settings/", include("settings.urls")),
    path("dashboard", DashBoardView.as_view()),
    # path('api/api-token-auth/', CustomAuthToken.as_view()),
    path("api-token-auth/", ObtainExpiringAuthToken.as_view()),
]

api_v2 = []

urlpatterns = [
    path("v1/", include(api_v1)),
    path("v2/", include(api_v2)),
]
