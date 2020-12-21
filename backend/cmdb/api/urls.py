

from .views import *


from django.contrib import admin
from django.urls import path, include
# from rest_framework.authtoken.views import obtain_auth_token
from authentication.views import CustomAuthToken, AssetData
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import include, path
# from rest_framework_expiring_authtoken.views import ObtainExpiringAuthToken
from authentication.views import ObtainExpiringAuthToken


app_name = 'api'

api_v1 = [
    path('admin/', admin.site.urls),
    # path('ws/', echo_once),
    path('', include('assets.urls')),
    path('', include('hosts.urls')),
    path('', include('vm.urls')),
    path('', include('tasks.urls')),
    path('', include('authentication.urls')),
    path('idrac/refresh_asset', api_refresh_asset, name='idrac-refresh-asset'),
    path('assetdata/', AssetData.as_view(), name='assetdata'),
    path('settings/', include('settings.urls')),
    path('dashboard', DashBoardView.as_view()),
    # path('api/api-token-auth/', CustomAuthToken.as_view()),
    path('api-token-auth/', ObtainExpiringAuthToken.as_view()),


]

api_v2 = [

]

urlpatterns = [
    path('v1/', include(api_v1)),
    path('v2/', include(api_v2)),
]

