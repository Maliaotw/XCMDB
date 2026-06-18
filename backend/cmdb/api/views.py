import datetime
import logging

from django.shortcuts import HttpResponse
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from assets import models as assets_models
from common import models as common_models
from hosts import models as hosts_models
from hosts import tasks

logger = logging.getLogger(__name__)


class DashBoardView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def recent_seven_days(self):
        from django.utils import timezone

        today = timezone.now().date()
        for i in range(7):
            yield today - datetime.timedelta(days=i)

    def get_count(self):
        counts = [
            {
                "title": "資產",
                "icon": "fa fa-asterisk",
                "count": assets_models.Asset.objects.all().count(),
                "color": "#2d8cf0",
            },
            {
                "title": "服務器",
                "icon": "fa fa-server",
                "count": hosts_models.Host.objects.filter(cate=1).count(),
                "color": "#ff9900",
            },
            {
                "title": "虛擬機",
                "icon": "fa fa-cloud",
                "count": hosts_models.Host.objects.filter(cate=2).count(),
                "color": "#19be6b",
            },
            {
                "title": "用戶",
                "icon": "fa fa-user",
                "count": common_models.UserProfile.objects.all().count(),
                "color": "#ed3f14",
            },
        ]

        return counts

    def get(self, request):

        list_week_day = list(self.recent_seven_days())
        list_week_day.reverse()

        asset_data = {"label": [i.strftime("%Y-%m-%d") for i in list_week_day], "latest_data": [], "create_data": []}

        for d in list_week_day:
            asset_data["latest_data"].append(assets_models.Asset.objects.filter(latest_date__date=d).count())
            asset_data["create_data"].append(assets_models.Asset.objects.filter(create_at__date=d).count())

        asset_type = {"label": [], "data": []}

        for i in assets_models.Asset.device_type_choices:
            asset_type["label"].append(i[1])
            asset_type["data"].append(assets_models.Asset.objects.filter(device_type_id=i[0]).count())

        data = {"asset_data": asset_data, "count": self.get_count(), "asset_type": asset_type}

        return Response(data)


# Create your views here.
def api_refresh_asset(request):
    """
    idrac 更新硬體信息
    :param request:
    :return:
    """

    id = request.GET.get("id")
    tasks.sync_idrac_hardware.delay(idrac_id=id)

    return HttpResponse("ok")
